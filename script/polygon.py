import os
import time
import requests
import pandas as pd
from tqdm import tqdm
from dotenv import load_dotenv

print('Loading API key')
load_dotenv()

API_KEY = os.getenv('POLYGON_KEY')

if API_KEY is None:
    raise ValueError('Missing POLYGON_KEY in .env file')

print('API key loaded')

# CONFIG
BASE_URL = 'https://api.massive.com/v1/open-close'
BASE = 'https://api.polygon.io'

UNDERLYING = 'SPY'

START_DATE = '2026-04-01'
END_DATE = '2026-07-01'

RATE_LIMIT_SLEEP = 12.2
DEBUG_N = 5

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# API Helper Functions

def get_option_chain(underlying, as_of):
    url = f'{BASE}/v3/reference/options/contracts'

    params = {
        'underlying_ticker': underlying,
        'as_of': as_of,
        'limit': 1000,
        'apiKey': API_KEY
    }

    r = requests.get(url, params=params)
    r.raise_for_status()
    return r.json()


def get_option_ohlc(ticker, date):
    url = f'{BASE_URL}/{ticker}/{date}'

    params = {
        'adjusted': 'true',
        'apiKey': API_KEY
    }

    r = requests.get(url, params=params)

    if r.status_code != 200:
        return None

    try:
        data = r.json()
    except Exception:
        return None

    if data.get('status') != 'OK':
        return None

    return data

def get_spy_history(start, end):
    url = f'{BASE}/v2/aggs/ticker/SPY/range/1/day/{start}/{end}'

    params = {
        'adjusted': 'true',
        'sort': 'asc',
        'limit': 50000,
        'apiKey': API_KEY
    }

    r = requests.get(url, params=params)
    r.raise_for_status()

    data = r.json().get('results', [])

    df = pd.DataFrame(data)

    df['date'] = pd.to_datetime(df['t'], unit='ms').dt.normalize()
    df['close'] = df['c']

    return dict(zip(df['date'], df['close']))

def select_atm_contracts(chain_results, spot_price, width=0.03, max_contracts=4):
    candidates = []

    for r in chain_results:
        ticker = r.get('ticker')
        strike = r.get('strike_price')

        if not ticker or strike is None:
            continue

        moneyness = abs(strike - spot_price) / spot_price

        if moneyness <= width:
            candidates.append((moneyness, ticker))

    candidates.sort(key=lambda x: x[0])

    return [t[1] for t in candidates[:max_contracts]]

# Create a date grid
dates = pd.bdate_range(START_DATE, END_DATE).normalize()

print('\nBuilding SPY history...')
spy_map = get_spy_history(START_DATE, END_DATE)


rows = []

pbar = tqdm(total=len(dates), desc='Rolling ATM OHLC')

for i, d in enumerate(dates):
    spot = spy_map.get(d, None)

    if spot is None:
        continue

    chain = get_option_chain(UNDERLYING, str(d.date()))
    results = chain.get('results', [])

    if not results:
        continue

    # Get options ATM
    atm_tickers = select_atm_contracts(results, spot)

    # Retrive OHLC data for ATM options
    for tkr in atm_tickers:

        data = get_option_ohlc(tkr, str(d.date()))

        if i < DEBUG_N:
            print(f'\nDEBUG: {d.date()} | {tkr}')
            print(data)

        if data and data.get('status') == 'OK':
            rows.append({
                'date': d.date(),
                'ticker': data.get('symbol'),
                'open': data.get('open'),
                'high': data.get('high'),
                'low': data.get('low'),
                'close': data.get('close'),
                'volume': data.get('volume'),
                'preMarket': data.get('preMarket'),
                'afterHours': data.get('afterHours'),
            })

        time.sleep(RATE_LIMIT_SLEEP)

    pbar.update(1)

pbar.close()

# Convert to DF and save

df = pd.DataFrame(rows)

if not df.empty:
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(['date', 'ticker']).reset_index(drop=True)

out_path = os.path.join(OUTPUT_DIR, 'spy_option.csv')
df.to_csv(out_path, index=False)

print(f'\nSaved to: {out_path}')
print(f'Rows: {len(df)}')
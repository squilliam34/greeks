from scipy.stats import norm
import numpy as np

def delta(S, T, r, K, sigma, option_type:str='call'):
    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T)/(sigma*np.sqrt(T))
    if option_type == 'call':
        return norm.cdf(d1)
    elif option_type == 'put':
        return norm.cdf(d1)-1

def gamma(S, T, r, K, sigma):
    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T)/(sigma*np.sqrt(T))
    return norm.pdf(d1)/(S*sigma*np.sqrt(T))

def vega(S, T, r, K, sigma):
    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T)/(sigma*np.sqrt(T))
    return S*norm.pdf(d1)*np.sqrt(T)

def theta(S, T, r, K, sigma, option_type:str='call'):
    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T)/(sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    if option_type == 'call':
        return -r*K*norm.cdf(d2)*np.exp(-r*T) - (sigma*S*norm.pdf(d1))/(2*np.sqrt(T))
    elif option_type == 'put':
        return r*K*norm.cdf(-d2)*np.exp(-r*T) - (sigma*S*norm.pdf(d1))/(2*np.sqrt(T))

def rho(S, T, r, K, sigma, option_type:str='call'):
    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T)/(sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    if option_type == 'call':
        return K*T*np.exp(-r*T)*norm.cdf(d2)
    elif option_type == 'put':
        return -K*T*np.exp(-r*T)*norm.cdf(-d2)
import numpy as np
from scipy.stats import norm
import numpy as np

def black_scholes(S, T, r, K, sigma, option_type:str='call'):
    d1 = (np.log(S/K) + (r + (sigma**2 / 2))*T) / sigma*np.sqrt(T)
    d2 = d1 - sigma*np.sqrt(T)
    if option_type == 'call':
            return (S*norm.cdf(d1) 
            - np.exp(-r*T)*K*norm.cdf(d2))
    elif option_type == 'put':
        return (np.exp(-r*T)*K*norm.cdf(-d2)
        - S*norm.cdf(-d1))
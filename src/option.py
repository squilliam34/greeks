"""Option class"""

import numpy as np
from scipy.stats import norm

class Option:

    def __init__(self, S, T, r, K, sigma, option_type:str='call'):
        if option_type not in ['call', 'put']:
            raise ValueError('option_type must be \"call\" or \"put\"')
        
        self.S = S
        self.T = T
        self.r = r
        self.K = K
        self.sigma = sigma
        self.option_type = option_type

        # Calculate d1 and d2 from Black-Scholes
        self.d1 = ((np.log(self.S/self.K) + (self.r + (self.sigma**2 / 2))*self.T) 
        / self.sigma*np.sqrt(self.T))

        self.d2 = self.d1 - self.sigma*np.sqrt(self.T)

    def black_scholes(self):
        """Calculates the price of the option according Black-Scholes"""
        if self.option_type == 'call':
            return (self.S*norm.cdf(self.d1) 
            - np.exp(-self.r*self.T)*self.K*norm.cdf(self.d2))
        elif self.option_type == 'put':
            return (np.exp(-self.r*self.T)*self.K*norm.cdf(-self.d2)
            - self.S*norm.cdf(-self.d1))
        

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
        @property
        def d1(self):
            return (
                np.log(self.S/self.K)
                + (self.r + 0.5*self.sigma**2)*self.T
            ) / (self.sigma*np.sqrt(self.T))

        @property
        def d2(self):
            return self.d1 - self.sigma*np.sqrt(self.T)

    def black_scholes(self):
        """Calculates the price of the option according Black-Scholes"""
        if self.option_type == 'call':
            return (self.S*norm.cdf(self.d1) 
            - np.exp(-self.r*self.T)*self.K*norm.cdf(self.d2))
        elif self.option_type == 'put':
            return (np.exp(-self.r*self.T)*self.K*norm.cdf(-self.d2)
            - self.S*norm.cdf(-self.d1))

    def delta(self):
        """Calculate delta, the change in an option's price w.r.t. the underlying"""
        if self.option_type == 'call':
            return norm.cdf(self.d1)
        elif self.option_type == 'put':
            return norm.cdf(self.d1)-1
        
    def gamma(self):
        """Calculate gamma, the change in an option's delta w.r.t. the underlying"""
        return norm.pdf(self.d1)/(self.S*self.sigma*np.sqrt(self.T))

    def vega(self):
        """Calculate vega, the change in an option's price w.r.t. implied volatility"""
        return self.S*norm.pdf(self.d1)*np.sqrt(self.T)

    def theta(self):
        """Calculate theta, the change in an option's price w.r.t. time"""
        if self.option_type == 'call':
            return (-self.r*self.K*norm.cdf(self.d2)*np.exp(-self.r*self.T) 
            - (self.sigma*self.S*norm.pdf(self.d1))/(2*np.sqrt(self.T)))

        elif self.option_type == 'put':
            return (self.r*self.K*norm.cdf(-self.d2)*np.exp(-self.r*self.T) 
            - (self.sigma*self.S*norm.pdf(self.d1))/(2*np.sqrt(self.T)))

    def rho(self):
        """Calculate rho, the change in an option's price w.r.t. the interest rate"""
        if self.option_type == 'call':
            return self.K*self.T*np.exp(-self.r*self.T)*norm.cdf(self.d2)
        elif self.option_type == 'put':
            return -self.K*self.T*np.exp(-self.r*self.T)*norm.cdf(-self.d2)
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

    ############## Calculate d1 and d2 from Black-Scholes ##############
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

    ############## Closed Form Greeks ##############
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

    ############## Finite difference greeks ##############
    def finite_diff_delta(self, h=0.01):
        """Calculate delta using the finite difference"""
        up = self._copy_with(S=self.S + h)
        down = self._copy_with(S=self.S - h)

        return (
            up.black_scholes()
            - down.black_scholes()
        ) / (2 * h)

    def finite_diff_gamma(self, h=0.01):
        """Calculate gamma using the finite difference"""
        up = self._copy_with(S=self.S + h)
        down = self._copy_with(S=self.S - h)

        return (
            up.black_scholes()
            - 2*self.black_scholes()
            + down.black_scholes()
        ) / h**2

    def finite_diff_vega(self, h=0.001):
        """Calculate vega using the finite difference"""
        up = self._copy_with(sigma=self.sigma + h)
        down = self._copy_with(sigma=self.sigma - h)

        return (
            up.black_scholes()
            - down.black_scholes()
        ) / (2*h)

    def finite_diff_theta(self, h=1/365):
        """Calculate theta using the finite difference"""
        up = self._copy_with(T=self.T + h)
        down = self._copy_with(T=self.T - h)

        return -(
            up.black_scholes()
            - down.black_scholes()
        ) / (2*h)

    def finite_diff_rho(self, h=0.0001):
        """Calculate rho using the finite difference"""
        up = self._copy_with(r=self.r + h)
        down = self._copy_with(r=self.r - h)

        return (
            up.black_scholes()
            - down.black_scholes()
        ) / (2*h)

    ############## Implied Volatility ##############
    def implied_vol_bisection(self, market_price, tol=1e-6, max_iter=100):
        """Calculate implied volatility using the bisection method"""
        low, high = 1e-6, 5.0

        for _ in range(max_iter):
            mid = (low + high) / 2

            test_opt = self._copy_with(sigma=mid)
            price = test_opt.black_scholes()

            if price > market_price:
                high = mid
            else:
                low = mid

            if abs(price - market_price) < tol:
                return mid

        return (low + high) / 2

    def implied_vol_newton(self, market_price, tol=1e-6, max_iter=50, initial_guess = 0.02):
        """Calculate implied volatility using Newton-Raphson method"""
        sigma = initial_guess
        for _ in range(max_iter):

            test_option = self._copy_with(sigma=sigma)

            price = test_option.black_scholes()
            vega = test_option.vega()

            diff = price - market_price

            if abs(diff) < tol:
                return sigma

            sigma -= diff / vega

    ############## Util functions ##############
    def _copy_with(self, **kwargs):
        params = {
            "S": self.S,
            "T": self.T,
            "r": self.r,
            "K": self.K,
            "sigma": self.sigma,
            "option_type": self.option_type
        }
        params.update(kwargs)
        return Option(**params)

    def __repr__(self):
        return (
            f"Option("
            f"S={self.S}, "
            f"K={self.K}, "
            f"T={self.T}, "
            f"sigma={self.sigma}, "
            f"type='{self.option_type}')"
        )

    def greeks(self):
        return {
            "delta": self.delta(),
            "gamma": self.gamma(),
            "vega": self.vega(),
            "theta": self.theta(),
            "rho": self.rho()
        }
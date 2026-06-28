# greeks

This project was an exercise I wanted to work on while working through the Akuna Options 101 course. I was fascinated by the concept of the greeks and their relationship across different times, strikes, and spots. Hoping to better understand them, I started this project to apply the concepts I learned while working through the Akuna Options 101 modules.

## Project Structure
### src
This directory contains my source files. The files `greeks.py` and `pricing.py` simply contain functions that calculate an option's price using Black-Scholes and its analytical greeks.

`option.py` contains an `Option` class. It stores an option's spot price, interest rate, strike price, time to expiry, and volatility to calculate its price and greeks through class methods. The class also contains methods for calculating greeks via finite differences and its implied volatility using the bisection method, Newton-Raphson method, and a hybrid approach of the 2.

`kalman_filter.py` contains a `KalmanFilter` class, that instantiates a Kalman Filter. In accordance with the filtering algorithm, a `KalmanFilter` has an observation matrix and transition matrix, as well as methods to predict future observations and update itself using the Kalman gain.

### notebooks
This directory contains notebooks where I ran experiments:
- `black_scholes.ipynb`: Where I first implemented options pricing using the Black-Scholes method and tested it visually to ensure that I impliemented it correctly.
- `greeks.ipynb`: I derived closed form formulas for each greek from the Black-Scholes formula and tested them in this notebook. Here, I was able to first see how each greek evolved across spot price for a fixed strike.
- `heatmaps.ipynb`: An extension of the greeks notebook. To better understand how the greeks evolve and how relationships between variables affect the greeks, I plotted heatmaps with contour lines to represent levels. The 3 relationships I examined where: spot price vs time, spot price vs strike price, and time vs "moneyness". Here, moneyness represents how "at-the-money" an option was for a given spot price (Moneyness = $\frac{S}{K}$). 
- `surfaces.ipynb`: Plots the various greeks as 3D surfaces across spot prices and time to expiry to examine the relationships between each greek and an option's spot price and time to expiry. I also tried to plot cross-greek relationships as surfaces. I plotted a $\Gamma$ surface across spot price and time to expiry, and colored it by $\Delta$ values. I repeated this process with $\Gamma$ and $\Theta$ and $\nu$ and $\Theta$. 
- `finite_diff.ipynb`: I calculated an option's greeks using a finite difference approach, incrementing various inputs and seeing how the price changed. Here, I plotted each greek's finite difference's convergence as the "bump" decreased, and compared it with "closed form" value (based off of Black-Scholes and using fixed inputs). Finally, I also plotted the error of the finite difference approach from the analytical calculation, which better showed how instability increased as the "bump" decreased.
- `implied_volatility.ipynb`:

### script
This directory contains a script to aggregate OHLC data for SPY options across April, May, and up to June 26th. The script identifies options ATM at each point in time, pulls their price data from `polygon.io`, and compiles it into a `DataFrame` that is then saved to a csv.

### data
This directory contains OHLC options data that I aggregated and downloaded using `polygon.io`
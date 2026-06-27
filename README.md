# greeks

This project was an exercise I wanted to work on while working through the Akuna Options 101 course. I was fascinated by the concept of the greeks and their relationship across different times, strikes, and spots. Hoping to better understand them, I started this project to apply the concepts I learned while working through the Akuna Options 101 modules.

## Project Structure

### data
This directory contains OHLC options data that I aggregated and downloaded using `polygon.io`

### notebooks
This directory contains notebooks where I ran experiments:
- `black_scholes.ipynb`: Where I first implemented options pricing using the Black-Scholes method and tested it visually to ensure that I impliemented it correctly.
- `greeks.ipynb`: I derived closed form formulas for each greek from the Black-Scholes formula and tested them in this notebook. Here, I was able to first see how each greek evolved across spot price for a fixed strike.
- `heatmaps.ipynb`: An extension of the greeks notebook. To better understand how the greeks evolve and how relationships between variables affect the greeks, I plotted heatmaps with contour lines to represent levels. The 3 relationships I examined where: spot price vs time, spot price vs strike price, and time vs "moneyness". Here, moneyness represents how "at-the-money" an option was for a given spot price (Moneyness = $\frac{S}{K}$). 
- `surfaces.ipynb`:
- `finite_diff.ipynb`: I calculated an option's greeks using a finite difference approach, incrementing various inputs and seeing how the price changed. Here, I plotted each greek's finite difference's convergence as the "bump" decreased, and compared it with "closed form" value (based off of Black-Scholes and using fixed inputs). Finally, I also plotted the error of the finite difference approach from the analytical calculation, which better showed how instability increased as the "bump" decreased.
- `implied_volatility.ipynb`:
# This is the first and the most basic strategy based on Price/Volume Data
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use("seaborn")

eurusd = pd.read_csv("eurusd.csv", parse_dates=["Date"], index_col="Date")

# Visualizing the data
eurusd.plot(figsize = (12, 8), title = "EUR/USD", fontsize = 12)
plt.show()

# Adding log returns
eurusd["returns"] = np.log(eurusd.div(eurusd.shift(1)))

# Dropping NaN
eurusd.dropna(inplace = True)

# Cumulative returns
eurusd["cumulative_returns"] = eurusd.returns.cumsum()
eurusd["cumulative_max"] = eurusd.cumulative_returns.cummax()

# Performance Matrix
annualized_returns = eurusd.returns.mean()*252
volatility = eurusd.returns.std() * np.sqrt(252)
drawdown = (eurusd["cumulative_max"] - eurusd["cumulative_returns"]).max()

# Essentials for a cross-over strategy
sma_s = 50
sma_l = 200

eurusd["SMA_S"] = eurusd.price.rolling(sma_s).mean()
eurusd["SMA_L"] = eurusd.price.rolling(sma_l).mean()

# Visualizing the data
eurusd.plot(figsize = (12, 8), title = "EUR/USD", fontsize = 12)
plt.show()
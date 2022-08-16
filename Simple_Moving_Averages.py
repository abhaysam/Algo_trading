# This is the first and the most basic strategy based on Price/Volume Data
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import product
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


# Positions
eurusd["position"] = np.where(eurusd["SMA_S"]>eurusd["SMA_L"],1,-1)


# Visualizing the data
eurusd.loc["2016",["price", "SMA_S", "SMA_L", "position"]].plot(figsize = (12, 8), title = "EUR/USD", fontsize = 12, secondary_y = "position")
plt.show()

# Returns
eurusd["returns"] = np.log(eurusd.price.div(eurusd.price.shift(1))) #buy and hold
eurusd["strategy"] = eurusd.position.shift(1)*eurusd["returns"] # long short
eurusd.dropna(inplace = True)

# Absolute performance
eurusd[["returns","strategy"]].sum() # in terms of absolute returns
eurusd[["returns","strategy"]].sum().apply(np.exp) # What 1 dollar invested would end up as

# Annualized performance
eurusd[["returns","strategy"]].mean()*252 #Annualized returns
eurusd[["returns","strategy"]].std()*np.sqrt(252) #Annualized risk

eurusd["creturns"] = eurusd["returns"].cumsum().apply(np.exp) #Cumulative retusn on 1 dollar invested for buy and hold
eurusd["cstrategy"] = eurusd["strategy"].cumsum().apply(np.exp) #Cumulative retusn on 1 dollar invested for long short

eurusd[["creturns","cstrategy"]].plot(figsize = (12,8), title = "EUR/USD - SMA {} | SMA {}".format(sma_s,sma_l))
plt.show()

# LS alpha obe B&H
# any strategy should atleast otperform B&H before costs considered, as such a straegy is worthless 
outperf = eurusd.cstrategy.iloc[-1]-eurusd.creturns.iloc[-1]

def test_strategy(SMA):
    eurusd = pd.read_csv("eurusd.csv", parse_dates=["Date"], index_col="Date")
    eurusd["returns"] = np.log(eurusd.price.div(eurusd.price.shift(1)))
    eurusd["SMA_S"] = eurusd.price.rolling(int(SMA[0])).mean()
    eurusd["SMA_L"] = eurusd.price.rolling(int(SMA[1])).mean()
    eurusd["position"] = np.where(eurusd["SMA_S"] > eurusd["SMA_L"], 1, -1)
    eurusd["strategy"] = eurusd.position.shift(1)*eurusd["returns"]
    eurusd.dropna(inplace= True)
    
    return np.exp(eurusd["strategy"].sum())
    
# Trying different combinations
SMA_S_range = range(10,50,1)
SMA_L_range = range(100,252,1)

# Forming all possible combinations of the SMAs
combinations = list(product(SMA_S_range, SMA_L_range))

results = []
for comb in combinations:
    results.append(test_strategy(comb))

best_performance = combinations[np.argmax(results)]

all_results = pd.DataFrame(data = combinations, columns= ["SMA_S", "SMA_L"])
all_results["performance"] = results
all_results.nlargest(10, "performance")
all_results.nsmallest(10, "performance")
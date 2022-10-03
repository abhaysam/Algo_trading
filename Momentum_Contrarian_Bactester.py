import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use("seaborn")

# Calling user defined functions
from data_downloader import data_downloader

input_variables = {'name':"intraday.csv"}
data = data_downloader('csv', input_variables)
data = data.set_index('time')

data["returns"] = np.log(data.div(data.shift(1)))

# Applying the our strategy. 
"""
Contrarian strategy:
    if the rolling window return is negative we buy 
    if the rolling window return is positive we sell
"""
# Defining the rolling window of three ticks (each tick is of 6 hours)
window = 3
data["position"] = -np.sign(data["returns"].rolling(window).mean())
data["strategy"] = data.position.shift(1)*data["returns"]
data["cstrategy"] = data["strategy"].cumsum().apply(np.exp)

# Buy and Hold strategy (returns and cumulative returns)
data["creturns"] = data["returns"].cumsum().apply(np.exp)

# Plotting the results:
data[["creturns","cstrategy"]].plot(figsize = (12, 8), title = "EUR/USD | Window = {}".format(window))

# Profit loss on the strategy
data.dropna(inplace = True)
data[["returns","strategy"]].sum().apply(np.exp)

to_plot = ["returns"]
for w in [1,2,3,5,10]:
    data["position{}".format(w)] = -np.sign(data["returns"].rolling(w).mean())
    data["strategy{}".format(w)] = data["position{}".format(w)].shift(1)*data["returns"]
    to_plot.append("strategy{}".format(w))

data[to_plot].dropna().cumsum().apply(np.exp).plot(figsize = (12,8))
plt.title("DJI Intraday - 6h bars", fontsize = 12)
plt.legend(fontsize = 12)
plt.show()
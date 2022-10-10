import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use("seaborn")

data = pd.read_csv("intraday.csv", parse_dates = ["time"], index_col = "time")

data.plot(figsize = (12,8))
plt.show()

data.loc["2019-08"].plot(figsize = (12,8))
plt.show()

data["returns"] = np.log(data.div(data.shift(1)))

#Constructing the Bollinger bands
SMA = 30
dev = 2

# First the moving average
data["SMA"] = data.price.rolling(SMA).mean()
data[["price", "SMA"]].plot(figsize = (12,8))
plt.show()

#Zooming in on 08/2019
data.loc["2019-08",["price", "SMA"]].plot(figsize = (12,8))
plt.show()

data["price"].rolling(SMA).std()
data["price"].rolling(SMA).std().plot(figsize =(12,8))
plt.show()

data["Lower"] = data["SMA"] - data["price"].rolling(SMA).std()*dev
data["Upper"] = data["SMA"] + data["price"].rolling(SMA).std()*dev
data[["price", "SMA","Lower","Upper"]].plot(figsize = (12,8))
plt.show()

#Zooming in on 08/2019
data.loc["2019-08",["price", "SMA","Lower","Upper"]].plot(figsize = (12,8))
plt.show()

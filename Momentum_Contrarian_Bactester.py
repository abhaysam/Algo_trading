import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
plt.style.use("seaborn")

data = pd.read_csv("intraday.csv", parse_dates=["time"], index_col = "time")
raw = yf.download("EURUSD=X", "2018-01-01","2019-12-30", interval = "1h").Close.to_frame()

window = 3
data["returns"] = np.log(data.div(data.shift(1)))
data["position"] = -np.sign(data["returns"].rolling(window).mean())
data["strategy"] = data.position.shift(1)*data["returns"]
data["creturns"] = data["returns"].cumsum().apply(np.exp)
data["cstrategy"] = data["strategy"].cumsum().apply(np.exp)
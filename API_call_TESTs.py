# Lets test the call to the API
#Importing essential libraries
import os
import time
import matplotlib.pyplot as plt
plt.style.use("seaborn")
import seaborn as sns
import yfinance as yf
import pandas as pd
import numpy as np
import tpqoa
import fxcmpy

#%% OANDA - Section 1: TEST-Calling the API

homedir = os.path.expanduser("~")
os.chdir('D:\Algorithmic trading\API Token')

oanda_api = tpqoa.tpqoa("oanda.cfg")
oanda_api.get_account_summary()

# Account details
oanda_account_type = oanda_api.account_type
oanda_account_id = oanda_api.account_id

# Tradable instruments
oanda_instruments = oanda_api.get_instruments()

#%% OANDA - Section 2: TEST-Getting the historical EUR-USD data
"""
    Granularity:
    H1 - hourly data
    H12 - 12 hours / half day 
    M1 - minutely data
    S5 - 5 seconds data 
    price:
    B - Bid Price
    A - Ask Price
"""
help(oanda_api.get_history)
oanda_eur_usd_history_bid = oanda_api.get_history(instrument = "EUR_USD", start= "2020-07-01", end = "2022-07-31", granularity = "D", price = "B")
oanda_eur_usd_history_ask = oanda_api.get_history(instrument = "EUR_USD", start= "2020-07-01", end = "2022-07-31", granularity = "D", price = "A")

# Streaming high frequency data
oanda_streaming_data = oanda_api.stream_data("EUR_USD", stop = 18)
# To Stop the stream
# oanda_api.stop_stream()

#%% OANDA - Section 3: TEST-Executing orders

# Passing a long position
oanda_api.create_order(instrument= "EUR_USD", units=1000,sl_distance=0.01) 

# closing the long position
oanda_api.create_order(instrument= "EUR_USD", units=-1000,sl_distance=0.01) 
oanda_api.get_account_summary()
oanda_api.get_transactions(tid=8)
oanda_api.print_transactions() #Generates PnL for the last few orders

# Passing a short-sell position
oanda_api.create_order(instrument= "EUR_USD", units=-1000,sl_distance=0.01) 

#%% FXCM - Section 4: TEST-Calling the API

fxcm_api = fxcmpy.fxcmpy(config_file = "fxcm.cfg")

# Account Summary
fxcm_account_details = fxcm_api.get_accounts()
fxcm_account_ids = fxcm_api.get_account_ids()
fxcm_account_instruments = fxcm_api.get_instruments()

#%% FXCM - Section 5: TEST-Getting the historical EUR-USD data

help(fxcm_api.get_candles)
fxcm_candlestick_data = fxcm_api.get_candles("EUR/USD", number = 10000)
fxcm_candlestick_data.info()

# If we need only Bid or Ask
fxcm_candlestick_data_bids = fxcm_api.get_candles("EUR/USD", number = 5, columns =["bids"])
fxcm_candlestick_data_hourly = fxcm_api.get_candles("EUR/USD",start= "2020-07-01", end = "2020-09-30", period = "H1", columns =["asks"]) # Remember FXCM restricts 10000 points only
fxcm_candlestick_data_minutely = fxcm_api.get_candles("EUR/USD",start= "2020-07-01", end = "2020-07-06", period = "m1", columns =["asks"]) # Remember FXCM restricts 10000 points only

# Streaming high frequency data
# Subscribe for the data
fxcm_api.subscribe_market_data("EUR/USD")
# Check all the subscribed data sets
fxcm_api.get_subscribed_symbols()
# Getting live prices
fxcm_api.get_last_price("EUR/USD")
fxcm_api.get_prices("EUR/USD") # ticks from the moment we subscribed for a particular intrument

# Generating the live stream
while True:
    time.sleep(1)
    print(fxcm_api.get_last_price("EUR/USD").name, fxcm_api.get_last_price("EUR/USD").Bid,
          fxcm_api.get_last_price("EUR/USD").Ask, sep = "|")

# Un-Subscribe for the data
fxcm_api.unsubscribe_market_data("EUR/USD")

# Easier way to stream data
def print_data(data, dataframe):
    print('%3d | %s | %s, %s, %s'
          % (len(dataframe), data['Symbol'],
             pd.to_datetime(int(data['Updated']), unit='ms'),
             data['Rates'][0], data['Rates'][1]))

fxcm_api.subscribe_market_data("EUR/USD", (print_data,))

fxcm_api.close()

#%% FXCM - Section 6: TEST-Executing orders
fxcm_api.get_open_positions()
fxcm_api.create_market_buy_order("EUR/USD", 10) #1 lot is 1000 position, so 10 orders means 10000 amount

# Generating the pnl for the orders
col = ["tradeId","amountK","currency","grossPL","isBuy"]
fxcm_api.get_open_positions()[col]

# Closing the position (REMEMBER, FXCM BY DEFAULT EXECUTES HEDGING AND NOT NETTING)
fxcm_api.create_market_sell_order("EUR/USD", 10) #tHIS WILL RESULT IN TWO OPEN POSITIONS PERFECTING HEDGING EACH OTHER

# Closing all positions
fxcm_api.close_all_for_symbol("EUR/USD")

# PnL of all closed positions
fxcm_api.get_closed_positions_summary()[col]
fxcm_api.close()

#%% Datetime - Section 7: Parsing data with pandas DataFrame
temp = pd.read_csv("temp.csv", parse_dates= ["datetime"], index_col= "datetime")
temp.loc["2015"] #Yearly
temp.loc["2015-05"] #Monthly
temp.loc["2015-05-20"] #Daily
temp.loc["2015-05-20 10:00:00"] #Hourly
temp.loc["2015-01-01" : "2015-12-31"] #By period

# Resampling by Day, EOD of Month, Start of a Month, EOD Year, Start of year and so on 
temp.resample("D").sum()
temp.resample("2H").first()
temp.resample("W").mean()
temp.resample("W-Wed").mean()
temp.resample("M").mean()
temp.resample("MS").mean()
temp.resample("MS", loffset="14D").mean()
temp.resample("Q").mean()
temp.resample("Q-Feb").mean()
temp.resample("Y").mean()
temp.resample("YS").mean()

#%% Importing data from Yahoo Finance
ticker = ["AAPL", "BA", "KO", "IBM", "DIS", "MSFT"]
stocks_data = yf.download(ticker, start = "2010-01-01", end = "2019-02-06")
# Savings as csv and back
# stocks_data.to_csv("stocks.csv")
# pd.read_csv("stocks.csv", header = [0,1], index_col = [0], parse_dates =[0])

# stocks_data.columns = stocks_data.columns.to_flat_index()

#%% Inspection and visualization of single stocks data

# Extracting the closing price of the stocks
close = stocks_data.loc[:,"Close"].copy()
close.plot()
plt.show()

# Normalizing the price series
normalized_data = close.div(close.iloc[0]).mul(100)
normalized_data.plot()
plt.show()

aapl = close.AAPL.copy().to_frame()
aapl["lag1"]=aapl.shift(periods = 1) #this just shifts the value by one period. This way we can compute the difference between the prices on the same day.
aapl["diff"] = aapl.AAPL.sub(aapl.lag1)
aapl["pct_chg"] = aapl.AAPL.div(aapl.lag1).sub(1).mul(100)

# Simplified
aapl["diff2"] = aapl.AAPL.diff(periods = 1)
aapl["pct_chg2"] = aapl.AAPL.pct_change(periods = 1).mul(100)

# Monthly returns of a stock
monthly_returns = aapl.AAPL.resample("BM").last().pct_change(periods = 1).mul(100) #BM for last business day of the month

# Plotting Apple returns
aapl = close.AAPL.copy().to_frame()
ret = aapl.AAPL.pct_change().dropna()
ret.plot(kind = "hist", bins = 100)
plt.show()

daily_mean_return = ret.mean()
var_daily_returns = ret.var()
volatility_daily = ret.std()
ann_mean_retrun = ret.mean()*252
ann_var_return =ret.var()*252
volatility_ann = ret.std()*np.sqrt(252)

#%% Inspection and visualization of all stocks data simultaneously

ret = close.pct_change().dropna()
summary = ret.describe().T.loc[:,["mean","std"]] #Daily stats
summary["mean"] = summary["mean"]*252
summary["std"] = summary["std"]*np.sqrt(252)

summary.plot(kind = "scatter", x = "std", y = "mean", figsize = (15,12), s = 50, fontsize = 15)
for i in summary.index:
    plt.annotate(i, xy=(summary.loc[i, "std"]+0.002, summary.loc[i, "mean"]+0.002), size = 15)
plt.xlabel("ann. Risk(std)", fontsize = 15)
plt.ylabel("ann. Return", fontsize = 15)
plt.title("Risk/Return", fontsize = 20)
plt.show()

# Correlation and covariance
ret.cov()
ret.corr()







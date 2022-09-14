import pandas as pd
import numpy as np

# To pull the data from yahoo finance
# import yfinance as yf
# Example pull: raw = yf.download(tickers = symbol, start = start, end = end, interval = interval).Close.to_frame()

# To pull the data from Oanda
import tpqoa 
api = tpqoa.tpqoa("oanda.cfg")
"""
Help for Oanda:
    https://developer.oanda.com/rest-live-v20/instrument-ep/
"""

def data_downloader(symbol, start, end, interval = "D", price = "M", frequency = None):
    # Several pulls needs to be made if the granularith is not daily
    raw = api.get_history(instrument = symbol,start = start, end = end, granularity = interval, price = price)
    print("We are pulling the data from OANDA")
    return raw
    
start = "2004-01-01"
# end = "2020-06-30"
end = "2004-06-30"
symbol = "EUR_USD"
data = data_downloader(symbol, start, end, "H1", 'B')
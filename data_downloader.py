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
    granularity_available = ['S5','S10','S15','S30','M1','M2','M4','M5','M10','M15','M30','H1','H2','H3','H4','H6','H8','H12','D','W']
    price_availabe = ['A','B','M']
    if interval not in granularity_available:
        raise Exception("This granularity is not availabe")
    if price not in price_availabe:
        raise Exception("This price is not availabe")
    print("We are pulling the data from OANDA")
    if interval == "D" or interval == "W" or interval == "M":
        raw = api.get_history(instrument = symbol,start = start, end = end, granularity = interval, price = price)
    else:        
        # Several pulls needs to be made if the granularith is not daily
        raw = api.get_history(instrument = symbol,start = start, end = end, granularity = interval, price = price)
    return raw
    
# start = "2004-01-01"
# # end = "2020-06-30"
# end = "2020-06-30"
# symbol = "EUR_USD"
# data = data_downloader(symbol, start, end, "W", 'B')
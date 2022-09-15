import pandas as pd
import numpy as np

# To pull the data from yahoo finance
import yfinance as yf
# Example pull: raw = yf.download(tickers = symbol, start = start, end = end, interval = interval).Close.to_frame()

# To pull the data from Oanda
import tpqoa 
api = tpqoa.tpqoa("oanda.cfg")
# Example pull: raw = api.get_history(instrument = "EUR_USD", start = "2005-01-01", end = "2010-01-30", granularity = "H1", price = 'A')
# Help for Oanda: https://developer.oanda.com/rest-live-v20/instrument-ep/


def data_downloader(platform, symbol, start, end, interval = None, price = None):
    if platform == 'yf':
        raw = yf.download(tickers = symbol, start = start, end = end, interval = interval).Close.to_frame()
    elif platform == 'oanda': 
        if interval == None or price == None:
            raise Exception("Oanda needs the granularity and price inputs")
        granularity_available = {'S5':0.6,
                                 'S10':0.6,
                                 'S15':0.6,
                                 'S30':0.6,
                                 'M1':0.6,
                                 'M2':0.6,
                                 'M4':0.6,
                                 'M5':0.6,
                                 'M10':0.6,
                                 'M15':0.6,
                                 'M30':0.6,
                                 'H1':0.6,
                                 'H2':0.6,
                                 'H3':0.6,
                                 'H4':0.6,
                                 'H6':0.6,
                                 'H8':0.6,
                                 'H12':0.6,
                                 'D':0.6,
                                 'W':0.6}
        price_availabe = ['A','B']
        if interval not in granularity_available:
            raise Exception("This granularity is not availabe")
        if price not in price_availabe:
            raise Exception("This price is not availabe")
        print("We are pulling the data from OANDA")
        if interval == "D" or interval == "W" or interval == "M":
            raw = api.get_history(instrument = symbol,start = start, end = end, granularity = interval, price = price)
        else:        
            # Several pulls needs to be made if the granularity is not daily
            raw = api.get_history(instrument = symbol,start = start, end = end, granularity = interval, price = price)
    return raw
    


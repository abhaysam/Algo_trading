import pandas as pd
import numpy as np
import yfinance as yf

start = "2004-01-01"
end = "2020-06-30"
end = "2004-12-25"
symbol = "EURUSD=X"

def data_downloader(symbol, start, end, interval = "1d", frequency = None):
    if interval == "1d":
        raw = yf.download(tickers = symbol, start = start, end = end, interval = interval).Close.to_frame()
    return raw
    

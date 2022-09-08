import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import product
plt.style.use("seaborn")


class SMABacktester():
    
    def __init__(self, symbol, SMA_S, SMA_L, start, end):
        self.symbol = symbol
        self.SMA_S = SMA_S
        self.SMA_L = SMA_L
        self.start = start
        self.end = end
        self.results = None
        self.get_data()

    def get_data(self):
        ''' Imports the data from forex_pairs.csv (source can be changed).
        '''
        raw = yf.download(self.symbol, self.start, self.end).Close.to_frame()
        raw = raw.rename(columns={'Close':'price'})
        raw['price'].to_frame().dropna()
        raw = raw.loc[self.start:self.end].copy()
        raw["returns"] = np.log(raw/raw.shift(1))
        raw["SMA_S"] = raw.price.rolling(self.SMA_S).mean()
        raw["SMA_L"] = raw.price.rolling(self.SMA_L).mean()
        self.data = raw
        return raw
    
    def set_parameters(self, SMA_S = None, SMA_L = None):
        if SMA_S is not None:
            self.SMA_S = SMA_S
            self.data["SMA_S"] = self.data.price.rolling(self.SMA_S).mean()
        if SMA_L is not None:
            self.SMA_L = SMA_L
            self.data["SMA_L"] = self.data.price.rolling(self.SMA_L).mean()
            
tester = SMABacktester("AUDEUR=X", 50,250,"2010-01-01","2019-12-31")    
tester.data.isna().sum()

tester.set_parameters(SMA_S = 25, SMA_L = 125)    
tester.data.isna().sum()

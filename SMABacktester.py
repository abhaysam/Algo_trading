import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import product
from data_downloader import data_downloader
plt.style.use("seaborn")

class SMABacktester():
    
    def __init__(self, symbol, SMA_S, SMA_L, start, end):
        """

        Parameters
        ----------
        symbol : str
            ticker symbol (should follow the yahoo finance standards).
        SMA_S : int
            moving window in days for shorter SMA.
        SMA_L : int
            moving window in days for lonbger SMA.
        start : str
            start date for data import.
        end : str
            end date for data import.

        Returns
        -------
        None.

        """
        self.symbol = symbol
        self.SMA_S = SMA_S
        self.SMA_L = SMA_L
        self.start = start
        self.end = end
        self.results = None
        self.get_data()
        self.prepare_data()
        
    def __repr__(self):
        return "SMABacktester(symbol = {}, SMA_S = {}, SMA_S = {}, start = {}, end = {}".format(self.symbol, self.SMA_S, self.SMA_L, self.start, self.end)

    def get_data(self):
        ''' Imports the data from forex_pairs.csv (source can be changed).
        '''
        input_varibales = {'symbol' : self.symbol,
                           'start' : self.start,
                           'end' : self.end,
                           'period':None}
        raw = data_downloader('yf', input_varibales).Close.to_frame()
        raw = raw.rename(columns={'Close':'price'})
        raw['price'].to_frame().dropna()
        raw = raw.loc[self.start:self.end].copy()
        raw["returns"] = np.log(raw/raw.shift(1))
        self.data = raw
    
    def prepare_data(self):
        ''' Prepare dataset with strategy specific columns.
        '''
        data = self.data.copy()
        data["SMA_S"] = data.price.rolling(self.SMA_S).mean()
        data["SMA_L"] = data.price.rolling(self.SMA_L).mean()
        self.data = data
    
    def set_parameters(self, SMA_S = None, SMA_L = None):
        ''' Allows user to change the standard variables.
        '''
        if SMA_S is not None:
            self.SMA_S = SMA_S
            self.data["SMA_S"] = self.data.price.rolling(self.SMA_S).mean()
        if SMA_L is not None:
            self.SMA_L = SMA_L
            self.data["SMA_L"] = self.data.price.rolling(self.SMA_L).mean()
            
    def test_strategy(self):
        ''' Runs the strategy.
        '''
        data = self.data.copy().dropna()
        data["position"] = np.where(data["SMA_S"] > data["SMA_L"],1,-1)
        data["strategy"] = data["position"].shift(1)*data["returns"]
        data.dropna(inplace = True)
        data["creturns"] = data["returns"].cumsum().apply(np.exp)
        data["cstrategy"] = data["strategy"].cumsum().apply(np.exp)
        self.results = data
        
        perf = data["cstrategy"].iloc[-1]
        outperf = perf - data["creturns"].iloc[-1]
        return round(perf, 6), round(outperf, 6)
    
    def plot_results(self):
        ''' Plots the results based on the current SMA_S and SMA_L.
        '''
        if self.results is None:
            print("Run test_strategy() first")
        else:
            title = "{} | SMA_S = {} | SMA_L = {}".format(self.symbol, self.SMA_S, self.SMA_L)
            self.results[["creturns", "cstrategy"]].plot(title=title)
            
    def optimize_parameters(self, SMA_S_range, SMA_L_range):
        ''' Tries the range of SMA_S and SMA_L in-order to find the global maxima.
        '''

        combinations = list(product(range(*SMA_S_range), range(*SMA_L_range)))
        
        # Testing all combinations
        results = []
        for combi in combinations:
            self.set_parameters(combi[0],combi[1])
            results.append(self.test_strategy()[0])
            
        best_perf = np.max(results) # Best performance
        opt = combinations[np.argmax(results)] # Optimal parameters  

        # run/set the optimal strategy
        self.set_parameters(opt[0], opt[1]) 
        self.test_strategy()

        # Create a df with all the results
        all_results = pd.DataFrame(data = combinations, columns = ["SMA_S", "SMA_S"]) 
        all_results["performance"] = results
        self.results_overview = all_results
    
        return opt, best_perf
        
# tester = SMABacktester("EURUSD=X", 50,200,"2004-01-01","2020-06-30")    
# tester.test_strategy()
# tester.optimize_parameters((10,50,1),(100,252,1))
# tester.plot_results()
# tester.results_overview

    





























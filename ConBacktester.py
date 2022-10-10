
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from data_downloader import data_downloader
plt.style.use("seaborn")

class ConBacktester():
    
    def __init__(self, symbol, window, start, end, fees = 0, ticker = None):
        """

        Parameters
        ----------
        symbol : str
            ticker symbol (should follow the yahoo finance standards).
        window : int
            rolling window of ticks (each tick is of 6 hours).
        start : str
            start date for data import.
        end : str
            end date for data import.
        fees : float
            transaction fees 

        Returns
        -------
        None.

        """
        self.symbol = symbol
        self.ticker = ticker
        self.window = window
        self.start = start
        self.end = end
        self.fees = fees
        self.results = None
        self.get_data()
        
    def __repr__(self):
        return "ConBacktester(symbol = {}, window = {}, start = {}, end = {}, fees ={}".format(self.symbol, self.window, self.start, self.end, self.fees)

    def get_data(self):
        ''' Imports the data from forex_pairs.csv (source can be changed).
        '''
        input_varibales = {'symbol' : self.symbol,
                           'start' : self.start,
                           'end' : self.end,
                           'period':None}
        raw = data_downloader('csv', input_varibales)
        raw = raw.set_index('time')
        if len(list(raw)) > 1 and self.ticker is None:
            print("The csv choosen has data for more than one asset which are {}. Please provide a ticker".format(len(raw)))
        elif len(list(raw)) > 1 and self.ticker is not None:
            raw = raw[[self.ticker]].dropna()
            raw = raw.rename(columns={self.ticker:'price'})
        else:
            raw = raw.dropna()
            raw = raw.rename(columns={list(raw)[0]:'price'})
        raw = raw.loc[self.start:self.end].copy()
        raw["returns"] = np.log(raw/raw.shift(1))
        self.data = raw 
            
    def test_strategy(self):
        ''' Runs the strategy.
        '''
        data = self.data.copy().dropna()
        data["position"] = -np.sign(data["returns"].rolling(self.window).mean())
        data["strategy"] = data.position.shift(1)*data["returns"]
        data.dropna(inplace = True)
        
        data["trades"] = data.position.diff().fillna(0).abs()
        data.trades.value_counts()        
        data["strategy"] = data.strategy - data.trades*self.fees

        
        data["creturns"] = data["returns"].cumsum().apply(np.exp) # Buy and Hold
        data["cstrategy"] = data["strategy"].cumsum().apply(np.exp) # Contrarian Strategy
        self.results = data
        
        perf = data["cstrategy"].iloc[-1]
        outperf = perf - data["creturns"].iloc[-1]
        return round(perf, 6), round(outperf, 6)
    
    def plot_results(self):
        ''' Plots the results based on the current window.
        '''
        if self.results is None:
            print("Run test_strategy() first")
        else:
            title = "{} | Winow = {}".format(self.symbol, self.window)
            self.results[["creturns", "cstrategy"]].plot(title=title)
            
    def optimize_parameters(self, window_range):
        ''' Tries various rolling windows in-order to find the global maxima.
            
        Parameters
        ----------
        
        window_range : tuple
            tuples of the form (start, end, step_size)
        '''
        windows = range(*window_range)
        
        # Testing all combinations
        results = []
        for window in windows:
            self.window = window
            results.append(self.test_strategy()[0])
        
        best_perf = np.max(results) #best performance
        opt = windows[np.argmax(results)] #Optimal performance
        
        #Set the optimal performance
        self.window = opt
        self.test_strategy()
        
        # Compiling all the results
        all_results = pd.DataFrame(data = {"window": windows, "performance": results})
        self.results_overview = all_results
            
        return opt, best_perf
        


    






























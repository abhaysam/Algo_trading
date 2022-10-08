
import numpy as np
import matplotlib.pyplot as plt
from data_downloader import data_downloader
plt.style.use("seaborn")

class ConBacktester():
    
    def __init__(self, symbol, window, start, end, fees):
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
        '''

        # Testing all combinations
        results = []
        to_plot = ["returns"]
        data = self.data.copy()
        for w in [1,2,3,5,10]:
            data["position{}".format(w)] = -np.sign(data["returns"].rolling(w).mean())
            data["strategy{}".format(w)] = data["position{}".format(w)].shift(1)*data["returns"]
            to_plot.append("strategy{}".format(w))
            results.append(self.test_strategy()[0])
            
        data = data[to_plot].dropna().cumsum().apply(np.exp)
        best_perf = np.max(data.iloc[-1,:].values)
        best_performing_window = window_range[np.argmax(data.iloc[-1,:].values)]
        
        # Plotting the results
        data.plot(figsize = (12,8))
        plt.title("Contrarian strategy results with various rolling windows - 6h bars", fontsize = 12)
        plt.legend(fontsize = 12)
        plt.show()
            
        return best_perf, best_performing_window
        


    






























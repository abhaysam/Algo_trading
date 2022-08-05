#Importing essential libraries

import matplotlib.pyplot as plt
plt.style.use("seaborn")
import yfinance as yf
import numpy as np


#%% Class for generating all the stats for a stock
class FinancialInstrument():
    '''Class to analyze Financial Instruments 
    
    Attribues
    ---------
    
    ticker: str
        ticker symbol for which we are generating all the stats and graphs
    start: str
        start date of the data
    end: str
        end date of the data 
        
        
    '''
    def __init__(self, ticker, start, end):
        self._ticker = ticker #This is a protected attribute. The prefix attribute is clear warning that it is not supposed to be changed. prefix attribute does not appear in dropdown menu, but can be access by using prefix (for example data._ticker, instead of data.ticker)
        self.start = start
        self.end = end
        self.get_data()
        self.log_returns()
    def __repr__(self): #repr stands for representation. Add comments that the user should know whenyou run this class
        return "FinancialInstrument(ticker = {}, start = {}, end = {})".format(self._ticker, self.start, self.end)   
    def get_data(self):
        '''Retrives data from Yahoo Fiance
        '''
        raw = yf.download(self._ticker, self.start, self.end).Close.to_frame()
        raw.rename(columns = {"Close":"price"}, inplace = True)
        self.data = raw
    def log_returns(self):
        '''Computes log returns
        '''
        self.data["log_returns"] = np.log(self.data.price/self.data.price.shift(1))
    def plot_prices(self):
        self.data.price.plot(figsize=(12,8))
        plt.title("Price Chart: {}".format(self._ticker), fontsize = 15)
    def plot_returns(self, kind = "ts"):
        ''' Plots log returns either as time series ("ts") or as histogram ("hist")
        '''
        if kind == "ts":            
            self.data.log_returns.plot(figsize=(12,8))
            plt.title("Returns:{}".format(self._ticker), fontsize = 15)
        elif kind == "hist":
            self.data.log_returns.hist(figsize=(12,8), bins = int(np.sqrt(len(self.data))))
            plt.title("Frequency of Returns:{}".format(self._ticker), fontsize = 15)
    def set_ticker(self, ticker = None): # Incase the ticker is overwritten
        if ticker is not None:
            self._ticker = ticker
            self.get_data()
            self.log_returns()
            
class RiskReturn(FinancialInstrument):

    # When we pass __init__(self, ticker, start, end), the child class RiskReturn overrides the parent class and since 
    # RiskReturn does not download data from yf, this will result in error, hence we need the super function
       
    def __init__(self, ticker, start, end, freq = None):
        self.freq = freq
        super().__init__(ticker, start, end) 
    def __repr__(self): #repr stands for representation. Add comments that the user should know whenyou run this class
        return "RiskReturn(ticker = {}, start = {}, end = {})".format(self._ticker, self.start, self.end)   
    def mean_return(self):
        ''' Calculates mean return
        '''
        if self.freq is None:
            return self.data.log_returns.mean()
        else:
            resampled_price = self.data.price.resample(self.freq).last()
            resampled_returns = np.log(resampled_price / resampled_price.shift(1))
            return resampled_returns.mean()   
    def std_returns(self):
        ''' Calculates the standard deviation of returns (risk)
        '''
        if self.freq is None:
            return self.data.log_returns.std()
        else:
            resampled_price = self.data.price.resample(self.freq).last()
            resampled_returns = np.log(resampled_price / resampled_price.shift(1))
            return resampled_returns.std()        
    def annualized_perf(self):
        ''' Calculates annulized return and risk
        '''
        mean_return = round(self.data.log_returns.mean() * 252, 3)
        risk = round(self.data.log_returns.std() * np.sqrt(252), 3)
        print("Return: {} | Risk: {}".format(mean_return, risk))
        
































    
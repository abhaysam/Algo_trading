import pandas as pd

# To pull the data from yahoo finance
import yfinance as yf
# Example pull: raw = yf.download(tickers = symbol, start = start, end = end, interval = interval).Close.to_frame()

# To pull the data from Oanda
import tpqoa 
api = tpqoa.tpqoa("oanda.cfg")
# Example pull: raw = api.get_history(instrument = "EUR_USD", start = "2005-01-01", end = "2010-01-30", granularity = "H1", price = 'A')
# Help for Oanda: https://developer.oanda.com/rest-live-v20/instrument-ep/


def data_downloader(platform, input_variables):
    if platform == 'yf':
        symbol = input_variables['symbol']
        start = input_variables['start']
        end = input_variables['end']
        period = input_variables['period']
        interval = input_variables['interval']
        valid_periods = ['1d','5d','1mo','3mo','6mo','1y','2y','5y','10y','ytd','max']
        valid_intervals = ['1m','2m','5m','15m','30m','60m','90m','1h','1d','5d','1wk','1mo','3mo']
        if period == None:
            period = '1d'
        elif period != None and period not in valid_periods:
            raise Exception("Please select an appropriate period")
        if interval == None:
            interval = '1d'
        elif interval != None and interval not in valid_intervals:
            raise Exception("Please select an appropriate interval")
        raw = yf.download(tickers = symbol, start = start, end = end, period = period, interval = interval)
    elif platform == 'oanda': 
        symbol = input_variables['symbol']
        start = input_variables['start']
        end = input_variables['end']
        interval = input_variables['interval']
        price = input_variables['price']
        if interval == None or price == None:
            raise Exception("Oanda needs the granularity and price inputs")
        valid_granularity =     {'S5':0.6,
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
        if interval not in valid_granularity:
            raise Exception("This granularity is not availabe")
        if price not in price_availabe:
            raise Exception("This price is not availabe")
        print("We are pulling the data from OANDA")
        if interval == "D" or interval == "W" or interval == "M":
            raw = api.get_history(instrument = symbol,start = start, end = end, granularity = interval, price = price)
        else:        
            # Several pulls needs to be made if the granularity is not daily
            raw = api.get_history(instrument = symbol,start = start, end = end, granularity = interval, price = price)
    elif platform == 'csv':
        csv_toload = input_variables['symbol']
        raw =  pd.read_csv(csv_toload)        
    return raw
    


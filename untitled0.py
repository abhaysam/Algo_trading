# -*- coding: utf-8 -*-
"""
Created on Sat Oct  8 12:40:33 2022

@author: abhay
"""
from data_downloader import data_downloader
import numpy as np

symbol = "intraday.csv"
start = "2004-01-01"
end = "2020-06-30"
input_varibales = {'symbol' : symbol,
                   'start' : start,
                   'end' : end,
                   'period':None}
raw = data_downloader('csv', input_varibales)
raw = raw.set_index('time')
raw['price'].to_frame().dropna()
raw = raw.loc[start:end].copy()
raw["returns"] = np.log(raw/raw.shift(1))
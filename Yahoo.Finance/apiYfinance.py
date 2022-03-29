# coding=utf-8

import pandas as pd
import yfinance as yf


data = pd.DataFrame(yf.download('SBRCY', '2022-01-01', '2022-03-17'))     # input date
# compiling DF from Yahoo Finance query by dates
print(data['Adj Close'].sum())  # get sum by parameter and output

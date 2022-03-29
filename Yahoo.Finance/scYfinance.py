# coding=utf-8

import requests
import pandas as pd
import json

URL = 'https://yfapi.net/v8/finance/spark'  # url api service
querystring = {'interval': '1d', 'range': '3mo', 'symbols': 'SBRCY'}  # request parameters # input date
headers = {'x-api-key': "TOKEN-YAHOO-FINANCE-API"}     # authorization by token
response = requests.request("GET", URL, headers=headers, params=querystring)    # request response
result = json.loads(response.text)  # response is formed in json
df = pd.DataFrame(result['SBRCY'])    # compiling DF from json result
df.drop(columns=['symbol', 'previousClose', 'chartPreviousClose',
                 'end', 'start', 'dataGranularity'], inplace=True)  # removal of excess

print(df['close'].sum())    # get sum by parameter and output

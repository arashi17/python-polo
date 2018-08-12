""" Bittrex API """

import requests
import json

api_url = 'https://bittrex.com/api/v1.1/'

def get_data():
  answer = requests.get(api_url + 'public/getmarketsummaries')
  json_ticker = answer.json()
  data_dict = {}
  for i in range(len(json_ticker['result'])):
    pair = json_ticker['result'][i]['MarketName']
    bid = json_ticker['result'][i]['Bid']
    ask = json_ticker['result'][i]['Ask']
    data_dict[pair] = [bid, ask]
  return data_dict

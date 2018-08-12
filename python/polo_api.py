""" Poloniex API """

import requests
import json

api_url = 'https://poloniex.com/public?command='

def get_data():
  answer = requests.get(api_url + 'returnTicker')
  json_ticker = answer.json()
  data_dict = {}
  for pair in json_ticker.keys():
    bid = float(json_ticker[pair]['highestBid'])
    ask = float(json_ticker[pair]['lowestAsk'])
    data_dict[pair] = [bid, ask]
  return data_dict
  
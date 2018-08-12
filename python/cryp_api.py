""" Cryptopia API """

import requests
import json

api_url = 'https://www.cryptopia.co.nz/api/'

def get_data():
  answer = requests.get(api_url + 'GetMarkets')
  json_ticker = answer.json()
  data_dict = {}
  for i in range(len(json_ticker['Data'])):
    pair = json_ticker['Data'][i]['Label']
    split_pair = pair.split('/')
    bid = json_ticker['Data'][i]['BidPrice']
    ask = json_ticker['Data'][i]['AskPrice']
    data_dict[pair] = [split_pair[1], split_pair[0], bid, ask]
  return data_dict

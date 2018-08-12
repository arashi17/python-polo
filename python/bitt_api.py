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
    split_pair = pair.split('-')
    bid = json_ticker['result'][i]['Bid']
    ask = json_ticker['result'][i]['Ask']
    data_dict[pair] = [split_pair[0], split_pair[1], bid, ask]
  return data_dict


def get_order_book(pair):
  answer = requests.get(api_url + 'public/getorderbook?market=' + pair + '&type=both')
  order_book = answer.json()
  bid_list = []
  ask_list = []
  price_list = {}
  for i in range(len(order_book['result']['buy'])):
    bid_list.append([order_book['result']['buy'][i]['Rate'], order_book['result']['buy'][i]['Quantity']])
  for i in range(len(order_book['result']['sell'])):
    ask_list.append([order_book['result']['sell'][i]['Rate'], order_book['result']['sell'][i]['Quantity']])
  price_list['Bid'] = bid_list
  price_list['Ask'] = ask_list
  return price_list

""" Bittrex API """

import requests
import json

api_url = 'https://bittrex.com/api/v1.1/'

def legend2pair(legend):
  split_legend = legend.split('!')
  pair = split_legend[0] + '-' + split_legend[1]
  return pair

def legend2pairinv(legend):
  split_legend = legend.split('!')
  pair = split_legend[1] + '-' + split_legend[0]
  return pair


def get_data():
  answer = requests.get(api_url + 'public/getmarketsummaries')
  json_ticker = answer.json()
  data_dict = {'Exchange' : 'bitt'}
  for i in range(len(json_ticker['result'])):
    pair = json_ticker['result'][i]['MarketName']
    split_pair = pair.split('-')
    bid = json_ticker['result'][i]['Bid']
    ask = json_ticker['result'][i]['Ask']
    data_dict[pair] = [split_pair[0], split_pair[1], bid, ask]
  return data_dict


def get_order_book(legend, depth):
  pair = legend2pair(legend)
  answer = requests.get(api_url + 'public/getorderbook?market=' + pair + '&type=both')
  order_book = answer.json()
  if order_book['success'] == False and order_book['message'] == 'INVALID_MARKET':
    pair = legend2pairinv(legend)
    answer = requests.get(api_url + 'public/getorderbook?market=' + pair + '&type=both')
    order_book = answer.json()
  bid_list = []
  ask_list = []
  price_list = {}
  for i in range(depth):
    bid_list.append([order_book['result']['buy'][i]['Rate'], order_book['result']['buy'][i]['Quantity']])
  for i in range(depth):
    ask_list.append([order_book['result']['sell'][i]['Rate'], order_book['result']['sell'][i]['Quantity']])
  price_list['Bid'] = bid_list
  price_list['Ask'] = ask_list
  return price_list

""" Cryptopia API """

import requests
import json

api_url = 'https://www.cryptopia.co.nz/api/'

def legend2pair(legend):
  split_legend = legend.split('!')
  pair = split_legend[0] + '_' + split_legend[1]
  return pair

def legend2pairinv(legend):
  split_legend = legend.split('!')
  pair = split_legend[1] + '_' + split_legend[0]
  return pair


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


def get_order_book(legend):
  pair = legend2pair(legend)
  answer = requests.get(api_url + 'GetMarketOrders/' + pair)
  order_book = answer.json()
  if order_book['Error'] != None:
    pair = legend2pairinv(legend)
    answer = requests.get(api_url + 'GetMarketOrders/' + pair)
    order_book = answer.json()
  print(order_book)
  bid_list = []
  ask_list = []
  price_list = {}
  for i in range(len(order_book['Data']['Buy'])):
    bid_list.append([order_book['Data']['Buy'][i]['Price'], order_book['Data']['Buy'][i]['Volume']])
  for i in range(len(order_book['Data']['Sell'])):
    ask_list.append([order_book['Data']['Sell'][i]['Price'], order_book['Data']['Sell'][i]['Volume']])
  price_list['Bid'] = bid_list
  price_list['Ask'] = ask_list
  return price_list
  
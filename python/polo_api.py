""" Poloniex API """

import requests
import json

api_url = 'https://poloniex.com/public?command='

def legend2pair(legend):
  split_legend = legend.split('!')
  pair = split_legend[0] + '_' + split_legend[1]
  return pair

def legend2pairinv(legend):
  split_legend = legend.split('!')
  pair = split_legend[1] + '_' + split_legend[0]
  return pair


def get_data():
  answer = requests.get(api_url + 'returnTicker')
  json_ticker = answer.json()
  data_dict = {}
  for pair in json_ticker.keys():
    split_pair = pair.split('_')
    bid = float(json_ticker[pair]['highestBid'])
    ask = float(json_ticker[pair]['lowestAsk'])
    data_dict[pair] = [split_pair[0], split_pair[1], bid, ask]
  return data_dict


def get_order_book(legend):
  pair = legend2pair(legend)
  answer = requests.get(api_url + 'returnOrderBook&currencyPair=' + pair + '&depth=30')
  order_book = answer.json()
  if 'error' in order_book:
    pair = legend2pairinv(legend)
    answer = requests.get(api_url + 'returnOrderBook&currencyPair=' + pair + '&depth=30')
    order_book = answer.json()
  bid_list = []
  ask_list = []
  price_list = {}
  for i in range(len(order_book['bids'])):
    bid_list.append([float(order_book['bids'][i][0]), order_book['bids'][i][1]])
  for i in range(len(order_book['asks'])):
    ask_list.append([float(order_book['asks'][i][0]), order_book['asks'][i][1]])
  price_list['Bid'] = bid_list
  price_list['Ask'] = ask_list
  return price_list

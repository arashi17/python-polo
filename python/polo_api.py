""" Poloniex API """

import requests
import json

from time import time
import hmac
import hashlib
import urllib.parse

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
  data_dict = {'Exchange' : 'polo'}
  for pair in json_ticker.keys():
    split_pair = pair.split('_')
    bid = float(json_ticker[pair]['highestBid'])
    ask = float(json_ticker[pair]['lowestAsk'])
    data_dict[pair] = [split_pair[0], split_pair[1], bid, ask]
  return data_dict


def get_order_book(legend, depth, inverted):
  pair = legend2pair(legend)
  answer = requests.get(api_url + 'returnOrderBook&currencyPair=' + pair + '&depth=' + str(depth))
  order_book = answer.json()
  if 'error' in order_book:
    pair = legend2pairinv(legend)
    answer = requests.get(api_url + 'returnOrderBook&currencyPair=' + pair + '&depth=' + str(depth))
    order_book = answer.json()
  bid_list = []
  ask_list = []
  # print(pair)
  # print(order_book)
  if inverted == True:
    price_dict = {'currency' : pair.split('_')[1]}
    for i in range(len(order_book['bids'])):
      bid_list.append([(1 / float(order_book['bids'][i][0])), order_book['bids'][i][1]])
    for i in range(len(order_book['asks'])):
      ask_list.append([(1 / float(order_book['asks'][i][0])), order_book['asks'][i][1]])
  else:
    price_dict = {'currency' : pair.split('_')[0]}
    for i in range(len(order_book['bids'])):
      bid_list.append([float(order_book['bids'][i][0]), order_book['bids'][i][1]])
    for i in range(len(order_book['asks'])):
      ask_list.append([float(order_book['asks'][i][0]), order_book['asks'][i][1]])
  price_dict['Bid'] = bid_list
  price_dict['Ask'] = ask_list
  return price_dict

class Polo:
  def __init__(self, api_key, api_secret):
    self.api_key = api_key
    self.api_secret = api_secret
    self.url = 'https://poloniex.com/tradingApi'

  def return_balances(self):
    payload = {'command': 'returnBalances', 'nonce': int(time() * 1000)}
    paybytes = urllib.parse.urlencode(payload).encode('utf8')
    sign = hmac.new(self.api_secret, paybytes, hashlib.sha512).hexdigest()
    headers = {'Key': self.api_key, 'Sign': sign}

    r = requests.post(self.url, headers = headers, data = payload)
    # print(r.json())

  def buy(self, pair, rate, amount):
    payload = {'command': 'buy', 'nonce': int(time() * 1000), 'currencyPair': pair, 'rate': rate, 'amount': amount}
    paybytes = urllib.parse.urlencode(payload).encode('utf8')
    sign = hmac.new(self.api_secret, paybytes, hashlib.sha512).hexdigest()
    headers = {'Key': self.api_key, 'Sign': sign}

    r = requests.post(self.url, headers = headers, data = payload)
    # print(r.json())

  def sell(self, pair, rate, amount):
    payload = {'command': 'sell', 'nonce': int(time() * 1000), 'currencyPair': pair, 'rate': rate, 'amount': amount}
    paybytes = urllib.parse.urlencode(payload).encode('utf8')
    sign = hmac.new(self.api_secret, paybytes, hashlib.sha512).hexdigest()
    headers = {'Key': self.api_key, 'Sign': sign}

    r = requests.post(self.url, headers = headers, data = payload)
    # print(r.json())
    
    
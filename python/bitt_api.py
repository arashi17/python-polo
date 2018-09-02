""" Bittrex API """

import requests
import json

from time import time
import hmac
import hashlib
import urllib.parse

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


def get_order_book(legend, depth, inverted):
  pair = legend2pair(legend)
  answer = requests.get(api_url + 'public/getorderbook?market=' + pair + '&type=both')
  order_book = answer.json()
  if order_book['success'] == False and order_book['message'] == 'INVALID_MARKET':
    pair = legend2pairinv(legend)
    answer = requests.get(api_url + 'public/getorderbook?market=' + pair + '&type=both')
    order_book = answer.json()
  bid_list = []
  ask_list = []
  # print(pair)
  # print(order_book)
  if inverted == True:
    price_dict = {'currency' : pair.split('-')[1]}
    for i in range(depth):
      bid_list.append([(1 / order_book['result']['buy'][i]['Rate']), order_book['result']['buy'][i]['Quantity']])
    for i in range(depth):
      ask_list.append([(1 / order_book['result']['sell'][i]['Rate']), order_book['result']['sell'][i]['Quantity']])
  else:
    price_dict = {'currency' : pair.split('-')[0]}
    for i in range(depth):
      bid_list.append([order_book['result']['buy'][i]['Rate'], order_book['result']['buy'][i]['Quantity']])
    for i in range(depth):
      ask_list.append([order_book['result']['sell'][i]['Rate'], order_book['result']['sell'][i]['Quantity']])
  price_dict['Bid'] = bid_list
  price_dict['Ask'] = ask_list
  return price_dict

class Bitt:
  def __init__(self, api_key, api_secret):
    self.api_key = api_key
    self.api_secret = api_secret
    self.url_market = 'https://bittrex.com/api/v1.1/market/'
    self.url_account = 'https://bittrex.com/api/v1.1/account/'

  def return_balance(self, currency):
    nonce = str(int(time() * 1000))
    url_add = 'getbalance?apikey=' + self.api_key + '&nonce=' + nonce + '&currency=' + currency
    url = self.url_account + url_add
    paybytes = url.encode('utf8')
    sign = hmac.new(self.api_secret, paybytes, hashlib.sha512).hexdigest()
    headers = {'apisign': sign}
    r = requests.post(url, headers = headers)
    balance = r.json()
    if balance['success'] == True:
      if balance['result']['Balance'] == None:
        return -1.0
      else:
        return balance['result']['Balance']
    else:
      return -1.0

  def buy(self, pair, rate, amount):
    nonce = str(int(time() * 1000))
    url_add = 'buylimit?apikey=' + self.api_key + '&nonce=' + nonce + '&market=' + pair + '&quantity=' + amount + '&rate=' + rate
    url = self.url_market + url_add
    paybytes = url.encode('utf8')
    sign = hmac.new(self.api_secret, paybytes, hashlib.sha512).hexdigest()
    headers = {'apisign': sign}
    r = requests.post(url, headers = headers)
    print(r.json())

  def sell(self, pair, rate, amount):
    nonce = str(int(time() * 1000))
    url_add = 'selllimit?apikey=' + self.api_key + '&nonce=' + nonce + '&market=' + pair + '&quantity=' + amount + '&rate=' + rate
    url = self.url_market + url_add
    paybytes = url.encode('utf8')
    sign = hmac.new(self.api_secret, paybytes, hashlib.sha512).hexdigest()
    headers = {'apisign': sign}
    r = requests.post(url, headers = headers)
    print(r.json())

""" Cryptopia API """

import requests
import json

api_url = 'https://www.cryptopia.co.nz/api/'

def get_cryp_data():
  answer = requests.get(api_url + 'GetMarkets')
  json_ticker = answer.json()
  return json_ticker

""" API Commands """
import requests
import json

api_urls = {'polo' : 'https://poloniex.com/public?command=', 'bitt' : 'https://bittrex.com/api/v1.1/', 'cryp' : 'https://www.cryptopia.co.nz/api/'}

def get_ticker(exchange):
	if(exchange == 'bitt'):
		answer = requests.get(api_urls['bitt'] + 'public/getmarketsummaries')
		ticker = answer.json()
	if(exchange == 'polo'):
		answer = requests.get(api_urls['polo'] + 'returnTicker')
		ticker = answer.json()
	if(exchange == 'cryp'):
		answer = requests.get(api_urls['cryp'] + 'GetMarkets')
		ticker = answer.json()
	return(ticker)


""" Data organization """
import re

def get_pairs(pairs_list, ticker, exchange):
	if exchange == 'bitt':
		for i in range(len(ticker['result']))
			pairs_list.append(ticker['result'][i]['MarketName'])
	if exchange == 'polo':
		for key in ticker.keys():
			pairs_list.append(key)
	if exchange == 'cryp':
		for i in range(len(ticker['Data'])):
			pairs_list.append(ticker['Data'][i]['Label'])

def add_pairs(pairs_dict, pairs_list, list_pos):
	for i in range(pairs_list):
		pairs_split = re.split('-|_|/')
		legend = pairs_split[0] + '!' + pairs_split[1]
		for key in pairs_dict[key]:
			if legend == key:
				if pairs_dict[key][list_pos - 1]

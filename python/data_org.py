""" Data organization """
import re

def get_pairs(ticker, exchange):
	pairs_list = []
	if exchange == 'bitt':
		for i in range(len(ticker['result'])):
			pairs_list.append(ticker['result'][i]['MarketName'])
	if exchange == 'polo':
		for key in ticker.keys():
			pairs_list.append(key)
	if exchange == 'cryp':
		for i in range(len(ticker['Data'])):
			pairs_list.append(ticker['Data'][i]['Label'])
	return(pairs_list)

def add_pairs(pairs_dict, pairs_list, list_pos):
	for i in range(len(pairs_list)):
		pairs_split = sorted(re.split('-|_|/', pairs_list[i]))
		legend = pairs_split[0] + '!' + pairs_split[1]
		found = False
		for key in pairs_dict.keys():
			if legend == key:  # pair is traded in another exchange
				legend_list = pairs_dict[key].insert(list_pos, pairs_list[i])
				found = True
				break
		if found == False:
			pairs = []
			for j in range(list_pos):
				pairs.append('')
			pairs.append(pairs_list[i])
			pairs_dict[legend] = pairs
	for key in pairs_dict.keys():
		if len(pairs_dict[key]) == list_pos:
			pairs_dict[key].insert(list_pos, '')
	return(pairs_dict)


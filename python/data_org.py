""" Data organization """
import re

def get_pairs(ticker, exchange):
	pairs_values_dict = {}
	pairs_list = []
	if exchange == 'bitt':
		for i in range(len(ticker['result'])):
			key = ticker['result'][i]['MarketName']
			bid = ticker['result'][i]['Bid']
			ask = ticker['result'][i]['Ask']
			pairs_values_dict[key] = [bid, ask]
			pairs_list.append(ticker['result'][i]['MarketName'])
	if exchange == 'polo':
		for key in ticker.keys():
			bid = float(ticker[key]['highestBid'])
			ask = float(ticker[key]['lowestAsk'])
			pairs_values_dict[key] = [bid, ask]
			pairs_list.append(key)
	if exchange == 'cryp':
		for i in range(len(ticker['Data'])):
			key = ticker['Data'][i]['Label']
			bid = ticker['Data'][i]['BidPrice']
			ask = ticker['Data'][i]['AskPrice']
			pairs_values_dict[key] = [bid, ask]
			pairs_list.append(ticker['Data'][i]['Label'])
	return(pairs_values_dict)

def add_pairs(pairs_dict, pairs_values_dict, list_pos):
	for key0 in pairs_values_dict.keys():
		pairs_split = sorted(re.split('-|_|/', key0))
		legend = pairs_split[0] + '!' + pairs_split[1]
		found = False
		for key in pairs_dict.keys():
			if legend == key:  # pair is traded in another exchange
				pairs_dict[legend][key0] = pairs_values_dict[key0]
				found = True
				break
		if found == False:
			pairs_dict[legend] = {key0 : pairs_values_dict[key0]}


	# 		pairs = []
	# 		for j in range(list_pos):
	# 			pairs.append('')
	# 		pairs.append(pairs_list[i])
	# 		pairs_dict[legend] = pairs
	# for key in pairs_dict.keys():
	# 	if len(pairs_dict[key]) == list_pos:
	# 		pairs_dict[key].insert(list_pos, '')
	return(pairs_dict)

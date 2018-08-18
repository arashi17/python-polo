""" Test file """

# import api_commands
# import data_org
# import calcs

# polo_ticker = api_commands.get_ticker('polo')
# bitt_ticker = api_commands.get_ticker('bitt')
# cryp_ticker = api_commands.get_ticker('cryp')

# polo_pairs_dict = data_org.get_pairs(polo_ticker, 'polo')
# bitt_pairs_dict = data_org.get_pairs(bitt_ticker, 'bitt')
# cryp_pairs_dict = data_org.get_pairs(cryp_ticker, 'cryp')

# pairs_dict = {}

# pairs_dict = data_org.add_pairs(pairs_dict, polo_pairs_dict, 0)
# pairs_dict = data_org.add_pairs(pairs_dict, bitt_pairs_dict, 1)
# pairs_dict = data_org.add_pairs(pairs_dict, cryp_pairs_dict, 2)

# calcs.opp_search(pairs_dict)

import cryp_api
import bitt_api
import polo_api
import org_data
import time
import json

# get data from all exchanges
polo = polo_api.get_data()
bitt = bitt_api.get_data()
cryp = cryp_api.get_data()

# print(bitt)

# compare between 2 exchanges
prices = org_data.compare_exc(polo, bitt)
# print(polo_bitt)
# prices = org_data.compare_exc(polo, cryp)
# print(polo_cryp)
# prices = org_data.compare_exc(bitt, cryp)
# print(bitt_cryp)

# polo_order_book = polo_api.get_order_book('ETC!BTC')
# print(polo_order_book)
# bitt_order_book = bitt_api.get_order_book('LTC!USDT')
# print(bitt_order_book)
# cryp_order_book = cryp_api.get_order_book('BTC!ETC')

# for legend in polo_bitt.keys():
#   print(legend)
#   if polo_bitt[legend][0] == '1':
#     bid = polo_api.get_order_book(legend, depth)['Bid']
#     ask = bitt_api.get_order_book(legend, depth)['Ask']
#   else:
#     bid = bitt_api.get_order_book(legend, depth)['Bid']
#     ask = polo_api.get_order_book(legend, depth)['Ask']
#   orders[legend] = [bid, ask]



with open('data.json', 'w') as outfile:
  json.dump(prices, outfile)
print("data.json file has been written")
print(prices)
  # print('%s: %d, %d' % (legend, bid, ask))


""" Data organization """
import cryp_api
import bitt_api
import polo_api

import re
from operator import itemgetter

""" Returns
    exc = 'polo', 'bitt', 'cryp' => Exchange
    legend = ex: 'BTC!ETH' => Pair in our convention
    depth = ex: 5 => Depth in the orders book to check
    order_type = 'Bid', 'Ask' => type of order to check
"""
def generic_get_order_book(exc, legend, depth, order_type):
  if exc == 'polo':
    p_type = polo_api.get_order_book(legend, depth)[order_type]
  if exc == 'bitt':
    p_type = bitt_api.get_order_book(legend, depth)[order_type]
  if exc == 'cryp':
    p_type = cryp_api.get_order_book(legend, depth)[order_type]
  return p_type

""" Returns a dict with opportunities between 2 exchanges

"""
def compare_exc(exc1, exc2):
  depth = 5
  equiv_pairs = {}
  orders = {}
  for exc1_key in exc1.keys():
    if exc1_key != 'Exchange':
      split1 = sorted(re.split('-|_|/', exc1_key))
      legend1 = split1[0] + '!' + split1[1]
      for exc2_key in exc2.keys():
        if exc2_key != 'Exchange':
          split2 = sorted(re.split('-|_|/', exc2_key))
          legend2 = split2[0] + '!' + split2[1]
          if legend1 == legend2:
            exc1_base = exc1[exc1_key][0]
            exc1_bid = exc1[exc1_key][2]
            exc1_ask = exc1[exc1_key][3]
            exc2_base = exc2[exc2_key][0]
            if exc1_base == exc2_base:
              exc2_bid = exc2[exc2_key][2]
              exc2_ask = exc2[exc2_key][3]
            else:
              exc2_bid = (1 / exc2[exc2_key][2])
              exc2_ask = (1 / exc2[exc2_key][3])
            if exc1_bid > exc2_ask:
              equiv_pairs[legend1] = [exc1['Exchange'], exc2['Exchange']]
            else:
              if exc2_bid > exc1_ask:
                equiv_pairs[legend1] = [exc2['Exchange'], exc1['Exchange']]

  for legend in equiv_pairs.keys():
    print(legend)
    bid = generic_get_order_book(equiv_pairs[legend][0], legend, depth, 'Bid')
    ask = generic_get_order_book(equiv_pairs[legend][1], legend, depth, 'Ask')
    bid.sort(key=itemgetter(0), reverse=True)
    ask.sort(key=itemgetter(0), reverse=False)

    orders[legend] = [bid, ask]

  return orders

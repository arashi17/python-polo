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
def generic_get_order_book(exc, legend, depth, order_type, inverted):
  if exc == 'polo':
    order_book = polo_api.get_order_book(legend, depth, inverted)
  if exc == 'bitt':
    order_book = bitt_api.get_order_book(legend, depth, inverted)
  if exc == 'cryp':
    order_book = cryp_api.get_order_book(legend, depth, inverted)
  p_type = [order_book['currency'], order_book[order_type]]
  return p_type

""" Returns a dict with opportunities between 2 exchanges

"""
def compare_exc(exc1, exc2):
  depth = 10
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
            inverted = False
            if exc1_base == exc2_base:
              exc2_bid = exc2[exc2_key][2]
              exc2_ask = exc2[exc2_key][3]
            else:
              exc2_bid = (1 / exc2[exc2_key][2])
              exc2_ask = (1 / exc2[exc2_key][3])
              inverted = True
            if exc1_bid > exc2_ask:
              equiv_pairs[legend1] = [exc1['Exchange'], exc2['Exchange'], False, inverted]
            else:
              if exc2_bid > exc1_ask:
                equiv_pairs[legend2] = [exc2['Exchange'], exc1['Exchange'], inverted, False]

  for legend in equiv_pairs.keys():
    bid_exchange = equiv_pairs[legend][0]
    ask_exchange = equiv_pairs[legend][1]
    bid_inverted = equiv_pairs[legend][2]
    ask_inverted = equiv_pairs[legend][3]
    order_book = generic_get_order_book(bid_exchange, legend, depth, 'Bid', bid_inverted)
    bid = order_book[1]
    # print("%s: %s" % (equiv_pairs[legend][0], order_book[0]))
    order_book = generic_get_order_book(ask_exchange, legend, depth, 'Ask', ask_inverted)
    ask = order_book[1]
    # print("%s: %s" % (equiv_pairs[legend][1], order_book[0]))
    bid.sort(key=itemgetter(0), reverse=True)
    ask.sort(key=itemgetter(0), reverse=False)
    currency = order_book[0]
    orders[legend] = [bid, ask, currency]

  return orders


""" Profit calculation

"""
def profit_calc(orders):
  total_profit = {}
  for legend in orders.keys():
    profit = 0
    i = 0
    j = 0
    not_max_profit = True
    bid_list = orders[legend][0]
    ask_list = orders[legend][1]
    currency = orders[legend][2]
    while not_max_profit:
      bid = bid_list[i]
      bid_price = bid[0]
      bid_vol = bid[1]
      ask = ask_list[j]
      ask_price = ask[0]
      ask_vol = ask[1]
      if bid_price > ask_price:
        order_vol = min(bid_vol, ask_vol)
        profit += order_vol * (bid_price - ask_price)
        bid[1] -= order_vol
        ask[1] -= order_vol
        if bid[1] == 0:
          if i == (len(bid_list) - 1):
            not_max_profit = False
          else:
            i += 1
        else:
          if j == (len(ask_list) - 1):
            not_max_profit = False
          else:
            j += 1
      else:
        not_max_profit = False
    total_profit[legend] = [profit, currency]
  return total_profit

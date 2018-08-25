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
            if opp_check(exc1['Exchange'], exc2['Exchange'], exc1_bid, exc2_ask):
              equiv_pairs[legend1] = [exc1['Exchange'], exc2['Exchange'], False, inverted]
            else:
              if opp_check(exc2['Exchange'], exc1['Exchange'], exc2_bid, exc1_ask):
                equiv_pairs[legend2] = [exc2['Exchange'], exc1['Exchange'], inverted, False]

  for legend in equiv_pairs.keys():
    bid_exchange = equiv_pairs[legend][0]
    ask_exchange = equiv_pairs[legend][1]
    bid_inverted = equiv_pairs[legend][2]
    ask_inverted = equiv_pairs[legend][3]
    order_book = generic_get_order_book(bid_exchange, legend, depth, 'Bid', bid_inverted)
    bid = order_book[1]
    if len(bid) == 0:
      break
    # print("%s: %s" % (equiv_pairs[legend][0], order_book[0]))
    order_book = generic_get_order_book(ask_exchange, legend, depth, 'Ask', ask_inverted)
    ask = order_book[1]
    if len(ask) == 0:
      break
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
    profit = 0.0
    i = 0
    j = 0
    # print('Legend: ' + legend)
    not_max_profit = True
    bid_list = orders[legend][0]
    ask_list = orders[legend][1]
    currency = orders[legend][2]
    # print('Bid List: ' + str(bid_list))
    # print('Ask List: ' + str(ask_list))
    # print('Currency: ' + currency)
    while not_max_profit:
      # print('Bid i: %d  Ask j: %d' % (i, j))
      bid = bid_list[i]
      bid_price = bid[0]
      bid_vol = bid[1]
      # print('Bid: ' + str(bid))
      ask = ask_list[j]
      ask_price = ask[0]
      ask_vol = ask[1]
      # print('Ask: ' + str(ask))
      # print('%.8f > %.8f' % (bid_price, ask_price))
      if bid_price > ask_price:
        order_vol = min(bid_vol, ask_vol)
        # print('Order Vol: %.8f' % order_vol)
        old_profit = profit
        # print('Profit: %.8f' % old_profit)
        profit += order_vol * (bid_price - ask_price)
        # print('Added: %.8f' % (profit - old_profit))
        bid_list[i][1] -= order_vol
        ask_list[j][1] -= order_vol
        # print('Bid List Updated: ' + str(bid_list[i][1]))
        # print('Ask List Updated: ' + str(ask_list[j][1]))
        if bid_list[i][1] <= 0:
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


""" Opportunity check

"""
def opp_check(exc_a, exc_b, bid, ask):
  if exc_a == 'polo' or exc_a == 'cryp':
    fee_exc_a = 0.002
  else:
    if exc_a == 'bitt':
      fee_exc_a = 0.0025
  if exc_b == 'polo' or exc_b == 'cryp':
    fee_exc_b = 0.002
  else:
    if exc_b == 'bitt':
      fee_exc_b = 0.0025
  bid = bid / (1 + fee_exc_a)
  ask = ask / (1 - fee_exc_b)
  if bid > ask:
    return True
  else:
    return False


""" Data organization """
import cryp_api
import bitt_api
import polo_api
import jeol

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
  if inverted:
    if order_type == 'Bid':
      order_type = 'Ask'
    else:
      if order_type == 'Ask':
        order_type = 'Bid'
  gen_order_book = [order_book['currency'], order_book[order_type]]
  return gen_order_book

""" Returns a dict with opportunities between 2 exchanges
    Input is output of api.get_data()
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
              exc2_bid = (1 / exc2[exc2_key][3])
              exc2_ask = (1 / exc2[exc2_key][2])
              inverted = True
            if opp_check(exc1['Exchange'], exc2['Exchange'], exc1_bid, exc2_ask):
              equiv_pairs[legend1] = [exc1['Exchange'], exc2['Exchange'], False, inverted, exc1_key, exc2_key]
            else:
              if opp_check(exc2['Exchange'], exc1['Exchange'], exc2_bid, exc1_ask):
                equiv_pairs[legend2] = [exc2['Exchange'], exc1['Exchange'], inverted, False, exc2_key, exc1_key]

  for legend in equiv_pairs.keys():
    bid_exchange = equiv_pairs[legend][0]
    ask_exchange = equiv_pairs[legend][1]
    bid_inverted = equiv_pairs[legend][2]
    ask_inverted = equiv_pairs[legend][3]
    bid_pair = equiv_pairs[legend][4]
    ask_pair = equiv_pairs[legend][5]
    order_book = generic_get_order_book(bid_exchange, legend, depth, 'Bid', bid_inverted)
    bid = order_book[1]
    if len(bid) == 0:
      continue
    # print("%s: %s" % (equiv_pairs[legend][0], order_book[0]))
    order_book = generic_get_order_book(ask_exchange, legend, depth, 'Ask', ask_inverted)
    ask = order_book[1]
    if len(ask) == 0:
      continue
    # print("%s: %s" % (equiv_pairs[legend][1], order_book[0]))
    bid.sort(key=itemgetter(0), reverse=True)
    ask.sort(key=itemgetter(0), reverse=False)
    currency = order_book[0]
    orders[legend] = [bid, ask, currency, bid_inverted, ask_inverted, bid_pair, ask_pair, bid_exchange, ask_exchange]

  return orders


""" Compare analysis

"""
def create_orders(compare, considered_pairs):
  orders = {}
  for legend in compare.keys():
    if legend in considered_pairs:
      bid_list = compare[legend][0]
      ask_list = compare[legend][1]
      currency = compare[legend][2]
      bid_inverted = compare[legend][3]
      ask_inverted = compare[legend][4]
      bid_pair = compare[legend][5]
      ask_pair = compare[legend][6]
      bid_exchange = compare[legend][7]
      ask_exchange = compare[legend][8]
      i = 0
      j = 0
      order_vol = 0.0
      order_bid = 0.0
      order_ask = 0.0
      still_running = True
      while still_running:
        bid = bid_list[i]
        bid_price = bid[0]
        bid_vol = bid[1]
        ask = ask_list[j]
        ask_price = ask[0]
        ask_vol = ask[1]
        if opp_check(bid_exchange, ask_exchange, bid_price, ask_price):
          vol = min(bid_vol, ask_vol)
          if order_bid == 0.0:
            order_bid = bid_price
          else:
            order_bid = min(order_bid, bid_price)
          if order_ask == 0.0:
            order_ask = ask_price
          else:
            order_ask = max(order_ask, ask_price)
          order_vol += vol
          print('Order Bid: %.8f, Order Ask: %.8f, Order Vol: %.8f' % (order_bid, order_ask, order_vol))
          bid_list[i][1] -= vol
          ask_list[j][1] -= vol
          if bid_list[i][1] <= 0:
            if i == (len(bid_list) - 1):
              still_running = False
            else:
              i += 1
          else:
            if j == (len(bid_list) - 1):
              still_running = False
            else:
              j += 1
        else:
          still_running = False
      orders[legend] = [bid_exchange, bid_pair, order_bid, bid_inverted, ask_exchange, ask_pair, order_ask, ask_inverted, order_vol]
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
        # old_profit = profit
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
def opp_check(exc_bid, exc_ask, bid, ask):
  if exc_bid == 'polo' or exc_bid == 'cryp':
    fee_exc_bid = 0.002
  else:
    if exc_bid == 'bitt':
      fee_exc_bid = 0.0025
  if exc_ask == 'polo' or exc_ask == 'cryp':
    fee_exc_ask = 0.002
  else:
    if exc_ask == 'bitt':
      fee_exc_ask = 0.0025
  bid = bid / (1 + fee_exc_bid)
  ask = ask / (1 - fee_exc_ask)
  if bid > ask:
    return True
  else:
    return False


def create_considered_list(currencies):
  considered_pairs = []
  for i in range(len(currencies)):
    for j in range((i + 1), len(currencies)):
      considered_pairs.append(currencies[i] + '!' + currencies[j])
      considered_pairs.append(currencies[j] + '!' + currencies[i])
  return considered_pairs


def get_balances(orders):
  balance = {}
  balances = {}
  for pair in orders.keys():
    split_pair1 = pair.split('!')[0]
    split_pair2 = pair.split('!')[1]
    bid_exchange = orders[pair][0]
    ask_exchange = orders[pair][4]
    if bid_exchange == 'polo' or ask_exchange == 'polo':
      polo = polo_api.Polo(jeol.polo_1(), jeol.polo_2())
      balance1 = polo.return_balance(split_pair1)
      balance2 = polo.return_balance(split_pair2)
      balance['polo'] = [balance1, split_pair1, balance2, split_pair2]
    if bid_exchange == 'bitt' or ask_exchange == 'bitt':
      bitt = bitt_api.Bitt(jeol.bitt_1(), jeol.bitt_2())
      balance1 = bitt.return_balance(split_pair1)
      balance2 = bitt.return_balance(split_pair2)
      balance['bitt'] = [balance1, split_pair1, balance2, split_pair2]
    if bid_exchange == 'cryp' or ask_exchange == 'cryp':
      cryp = cryp_api.Cryp(jeol.cryp_1(), jeol.cryp_2())
      balance1 = cryp.return_balance(split_pair1)
      balance2 = cryp.return_balance(split_pair2)
      balance['cryp'] = [balance1, split_pair1, balance2, split_pair2]
    balances[pair] = balance
  return balances


def check_balances(balances, orders):
  for pair in orders.keys():
    bid_exchange = orders[pair][0]



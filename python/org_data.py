""" Data organization """

import re

def compare_exc(exc1, exc2):
  equiv_pairs = {}
  for exc1_key in exc1.keys():
    split1 = sorted(re.split('-|_|/', exc1_key))
    legend1 = split1[0] + '!' + split1[1]
    for exc2_key in exc2.keys():
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
        if (exc1_bid > exc2_ask) or (exc2_bid > exc1_ask):
          equiv_pairs[legend1] = [exc1[exc1_key], exc1_bid, exc2[exc2_key], exc2_bid]

  return equiv_pairs


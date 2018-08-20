""" Calculates profit from json data
"""

import requests
import json
import os

path = './data/'
loaded_data = []
total_profit = {}
for filename in os.listdir(path):
  with open(path + filename) as f:
    loaded_data.append(json.load(f))

for i in range(len(loaded_data)):
  for legend in loaded_data[i].keys():
    if legend in total_profit.keys():
      total_profit[legend][0] += loaded_data[i][legend][0]
    else:
      total_profit[legend] = [loaded_data[i][legend][0], loaded_data[i][legend][1]]
    loaded_data[i][legend][0] = 0
    j = 1
    while (i + j) < (len(loaded_data) - 1):
      if legend in loaded_data[i + j].keys():
        total_profit[legend][0] += loaded_data[i + j][legend][0]
        loaded_data[i + j][legend][0] = 0
      j += 1

consolidated = {}
for legend in total_profit:
  if total_profit[legend][1] in consolidated.keys():
    consolidated[total_profit[legend][1]] += total_profit[legend][0]
  else:
    consolidated[total_profit[legend][1]] = total_profit[legend][0]

with open(path + 'analyse.json', 'w') as outcome:
  json.dump(total_profit, outcome)

with open(path + 'consolidated.json', 'w') as outcome:
  json.dump(consolidated, outcome)

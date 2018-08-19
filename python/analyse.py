""" Calculates profit from json data
"""

import json
import os

path = './data1/'
loaded_data = []
total_profit = {}
for filename in os.listdir(path):
  with open(path + filename) as f:
    loaded_data.append(json.load(f))

for i in range(len(loaded_data)):
  for legend in loaded_data[i].keys():
    if legend in total_profit.keys():
      total_profit[legend] += loaded_data[i][legend]
    else:
      total_profit[legend] = loaded_data[i][legend]
    loaded_data[i][legend] = 0
    j = 1
    while (i + j) < (len(loaded_data) - 1):
      if legend in loaded_data[i + j].keys():
        total_profit[legend] += loaded_data[i + j][legend]
        loaded_data[i + j][legend] = 0
      j += 1

with open(path + 'analyse.json', 'w') as outcome:
  json.dump(total_profit, outcome)



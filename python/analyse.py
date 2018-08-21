""" Calculates profit from json data
"""

import argparse
import fnmatch
import requests
import json
import os

parser = argparse.ArgumentParser(description = 'Generate report from all files in the folder.')
parser.add_argument('--path')
parser.add_argument('--blues')
args = vars(parser.parse_args())


path = args['path']
loaded_data = []
loaded_data_filtered = []
temp_dict = {}
total_profit = {}
removed_pairs = ['BITS!BTC', 'BTC!BITS', 'BTC!BTM', 'BTM!BTC', 'BTC!FCT', 'FCT!BTC', 'BTC!BTG', 'BTG!BTC', 'EMC2!BTC', 'BTC!EMC2', 'EOS!BTC', 'BTC!EOS']
considered = ['BTC', 'USDT', 'ETH', 'ETC', 'LTC', 'XMR', 'DASH', 'XRP']
considered_list = []
for i in range(len(considered)):
  for j in range((i + 1), len(considered)):
    considered_list.append(considered[i] + '!' + considered[j])
    considered_list.append(considered[j] + '!' + considered[i])
filelist = os.listdir(path)
filtered_filelist = fnmatch.filter(filelist, 'res_*')
for filename in filelist:
  if filename not in filtered_filelist:
    with open(path + filename) as f:     
      loaded_data.append(json.load(f))
print(args['blues'])
if args['blues'] == 'Y':
  for i in range(len(loaded_data)):
    for legend in loaded_data[i].keys():
      if legend in considered_list:
        temp_dict[legend] = loaded_data[i][legend]
    loaded_data_filtered.append(temp_dict)
else:
  loaded_data_filtered = loaded_data.copy()

for i in range(len(loaded_data_filtered)):
  for legend in loaded_data_filtered[i].keys():
    if legend not in removed_pairs:
      if legend in total_profit.keys():
        total_profit[legend][0] += loaded_data_filtered[i][legend][0]
      else:
        total_profit[legend] = [loaded_data_filtered[i][legend][0], loaded_data_filtered[i][legend][1]]
      loaded_data_filtered[i][legend][0] = 0
      j = 1
      while (i + j) < (len(loaded_data_filtered) - 1):
        if legend in loaded_data_filtered[i + j].keys():
          total_profit[legend][0] += loaded_data_filtered[i + j][legend][0]
          loaded_data_filtered[i + j][legend][0] = 0
        j += 1

consolidated = {}
for legend in total_profit:
  if total_profit[legend][1] in consolidated.keys():
    consolidated[total_profit[legend][1]] += total_profit[legend][0]
  else:
    consolidated[total_profit[legend][1]] = total_profit[legend][0]

with open(path + 'res_analyse.json', 'w') as outcome:
  json.dump(total_profit, outcome)

with open(path + 'res_consolidated.json', 'w') as outcome:
  json.dump(consolidated, outcome)

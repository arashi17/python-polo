""" Execute """

import argparse
import os
import cryp_api
import bitt_api
import polo_api
import org_data
import json
import time

parser = argparse.ArgumentParser(description='Run.')
parser.add_argument('--scan_time', type=float)
parser.add_argument('--interval', type=int)
parser.add_argument('--path')

args = vars(parser.parse_args())

def run(i, path):
  polo = polo_api.get_data()
  bitt = bitt_api.get_data()
  cryp = cryp_api.get_data()

  prices = org_data.compare_exc(polo, bitt)
  # with open(path + 'pb.json', 'w') as outfile:
  #   json.dump(prices, outfile)
  total_profit = org_data.profit_calc(prices)
  with open(path + 'polo_bitt' + str(i) + '.json', 'w') as outfile:
    json.dump(total_profit, outfile)

  prices = org_data.compare_exc(polo, cryp)
  # with open(path + 'pc.json', 'w') as outfile:
  #   json.dump(prices, outfile)
  total_profit = org_data.profit_calc(prices)
  with open(path + 'polo_cryp' + str(i) + '.json', 'w') as outfile:
    json.dump(total_profit, outfile)

  prices = org_data.compare_exc(bitt, cryp)
  # with open(path + 'bc.json', 'w') as outfile:
  #   json.dump(prices, outfile)
  total_profit = org_data.profit_calc(prices)
  with open(path + 'bitt_cryp' + str(i) + '.json', 'w') as outfile:
    json.dump(total_profit, outfile)


path = args['path']
if not os.path.exists(path):
  os.makedirs(path)
total_scan_time = args['scan_time'] # in hours
interval = args['interval'] # in minutes
scans = total_scan_time * 60 / interval
start_time = time.time()
for i in range(int(scans)):
  run_time = time.time()
  print('Run %d out of %d' % (i + 1, int(scans)))
  run(i, path)
  elapsed_time = time.time() - run_time
  interval_sec = (interval * 60) - elapsed_time
  if interval_sec <= 0:
    interval_sec = 10
  print('Sleeping for %d seconds' % interval_sec)
  if i < (int(scans) - 1):
    time.sleep(interval_sec)
  end_run = time.time() - run_time
  print('Run %d took %d seconds' % (i + 1, end_run))
total_time = (time.time() - start_time) / 60
print('Total time: %d minutes' % int(total_time))

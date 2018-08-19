""" Execute """

import cryp_api
import bitt_api
import polo_api
import org_data
import json
import time

def run(i):
  polo = polo_api.get_data()
  bitt = bitt_api.get_data()
  cryp = cryp_api.get_data()

  prices = org_data.compare_exc(polo, bitt)
  total_profit = org_data.profit_calc(prices)
  with open('./data/polo_bitt' + str(i) + '.json', 'w') as outfile:
    json.dump(total_profit, outfile)

  prices = org_data.compare_exc(polo, cryp)
  total_profit = org_data.profit_calc(prices)
  with open('./data/polo_cryp' + str(i) + '.json', 'w') as outfile:
    json.dump(total_profit, outfile)

  prices = org_data.compare_exc(bitt, cryp)
  total_profit = org_data.profit_calc(prices)
  with open('./data/bitt_cryp' + str(i) + '.json', 'w') as outfile:
    json.dump(total_profit, outfile)


total_scan_time = 3 # in hours
interval = 10 # in minutes
scans = total_scan_time * 60 / interval
start_time = time.time()
for i in range(int(scans)):
  run_time = time.time()
  print('Run %d out of %d' % (i + 1, int(scans)))
  run(i)
  print('Sleeping for %d minutes' % interval)
  time.sleep(interval * 60)
  end_run = (time.time() - run_time) / 60
  print('Run %d took %d minutes' % (i + 1, int(end_run)))
total_time = (time.time() - start_time) / 60
print('Total time: %d minutes' % int(total_time))

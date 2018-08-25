
import polo_api
import bitt_api
import org_data
import json

""" Get data
polo = polo_api.get_data()
bitt = bitt_api.get_data()

prices = org_data.compare_exc(polo, bitt)
with open('./abc/pb.json', 'w') as f:
  json.dump(prices, f)
"""

# with open('./abc/pbe.json') as f:
#   data = json.load(f)

# profit = org_data.profit_calc(data)

# with open('./abc/pb_profit.json', 'w') as f:
#   json.dump(profit, f)

polo = polo_api.Polo('7TJSQLIZ-AGGYSMW4-8Y14JIX1-769GNMKK', b'bdea89070e905aad83ff63b6845fe38be94b33506df9ccbf8f9d702b6d94bfbc0aceebbff5e0b8ff1d33d4f38a82efd925ce80342e089c7fb4ecb9bb8eb76eab')

# polo.return_balances()


# polo = polo_api.get_data()
# for key in polo.keys():
#   if key == 'BTC_ETH':
#     print(polo[key])

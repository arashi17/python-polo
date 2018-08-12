""" Test file """

# import api_commands
# import data_org
# import calcs

# polo_ticker = api_commands.get_ticker('polo')
# bitt_ticker = api_commands.get_ticker('bitt')
# cryp_ticker = api_commands.get_ticker('cryp')

# polo_pairs_dict = data_org.get_pairs(polo_ticker, 'polo')
# bitt_pairs_dict = data_org.get_pairs(bitt_ticker, 'bitt')
# cryp_pairs_dict = data_org.get_pairs(cryp_ticker, 'cryp')

# pairs_dict = {}

# pairs_dict = data_org.add_pairs(pairs_dict, polo_pairs_dict, 0)
# pairs_dict = data_org.add_pairs(pairs_dict, bitt_pairs_dict, 1)
# pairs_dict = data_org.add_pairs(pairs_dict, cryp_pairs_dict, 2)

# calcs.opp_search(pairs_dict)

import cryp_api
import bitt_api
import polo_api
import org_data
import time


polo = polo_api.get_data()
bitt = bitt_api.get_data()
cryp = cryp_api.get_data()

polo_bitt = org_data.compare_exc(polo, bitt)
polo_cryp = org_data.compare_exc(polo, cryp)
bitt_cryp = org_data.compare_exc(bitt, cryp)
# print(polo_bitt)
# print(polo_cryp)
print(bitt_cryp)

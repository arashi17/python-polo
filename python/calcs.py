""" Calculations """

def opp_search(pairs_dict):
	for legend in pairs_dict.keys():
		if len(pairs_dict[legend]) > 1:
			pair_list = []
			bid_list = []
			ask_list = []
			for pair in pairs_dict[legend].keys():
				pair_list.append(pair)
				bid_list.append(pairs_dict[legend][pair][0])
				ask_list.append(pairs_dict[legend][pair][1])
			found_pair = []
			# print(pair_list)
			for i in range(len(bid_list)):
				bid_price = bid_list[i]
				bid_inverted = False
				if bid_price < 1:
					bid_price = 1 / bid_price
					bid_inverted = True
				for j in range(len(ask_list)):
					ask_price = ask_list[j]
					ask_inverted = False
					if ask_price < 1:
						ask_price = 1 / ask_price
						ask_inverted = True
					if bid_inverted and ask_inverted:
						if bid_price < ask_price:
							found_pair.append(pair_list[i])
							print(pair_list)
							print(str(i) + ' ' + str(j) + ' ' + str(bid_list[i]) + ' ' + str(ask_list[j]) + ' ' + str(bid_price) + ' ' + str(ask_price))
						break
					else:
						if bid_price > ask_price:
							found_pair.append(pair_list[i])
							print(pair_list)
							print(str(i) + ' ' + str(j) + ' ' + str(bid_list[i]) + ' ' + str(ask_list[j]) + ' ' + str(bid_price) + ' ' + str(ask_price))
						break
		# print(found_pair)

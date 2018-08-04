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
				for j in range(len(ask_list)):
					if bid_list[i] > ask_list[j]:
						found_pair.append(pair_list[i])
						print(pair_list)
						print(str(i) + ' ' + str(j) + ' ' + str(bid_list[i]) + ' ' + str(ask_list[j]))
					break
		# print(found_pair)

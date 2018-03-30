from Voter import Voter


if __name__ == '__main__':

	message = "This is just a test."

	# Create a root voter, ie. is passed no data
	root_voter = Voter(10,5)
	root_voter_keys = root_voter.generate_scheme()

	# Create a sub voter, given the first key from the root_voter keys
	sub_voter = Voter(3,2)
	sub_voter_keys = sub_voter.generate_scheme(root_voter_keys[0][1])

	# For testing purposes remove key used to create the sub_voter
	root_voter_keys = root_voter_keys[1:]

	# Now reconstruct the deleted key from the sub_voter
	############## PROBLEM HERE: Even though the key can be reconstructed the original x value was lost forever ################
	# Possible Solution: Pass the x value in when constructing the sub_voter, so data in generate_scheme is a tuple instead.
	for i in range(sub_voter.k):
		print(sub_voter_keys[i])
		sub_voter.add_key_to_signature(root_voter_keys[i])

	rebuilt_key = sub_voter.values[-1]

	print(rebuilt_key)

	print('')

	# Now go through a vote on root_voter
	for i in range(root_voter.k):
		print(root_voter_keys[i])
		root_voter.add_key_to_signature(root_voter_keys[i])

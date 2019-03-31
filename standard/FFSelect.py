import numpy as np
from scipy import stats

def FFSelect_cycle(seq, targets, n_FF_selected):
	# input:
	# seq, targets, n_FF_selected
	# output:
	# indices of the selected FFs

	# SP_1 SP_0: signal probabilities, shape(#cycle, #FF)
	SP_1 = np.zeros((seq.shape[1], seq.shape[2]))
	SP_0 = np.zeros((seq.shape[1], seq.shape[2]))
	count_1 = 0
	count_0 = 0
	for i in range(seq.shape[0]):
		if targets[i] == 1:
			SP_1 = SP_1 + seq[i]
			count_1 = count_1 + 1
		else:
			SP_0 = SP_0 + seq[i]
			count_0 = count_0 + 1

	SP_1 = SP_1 / count_1
	SP_0 = SP_0 / count_0
	"""
	file_SP_1 = open('file_cycle_SP_1.txt', 'w')
	for i in range(SP_1.shape[0]):
		for j in range(SP_1.shape[1]):
			file_SP_1.write(str(SP_1[i][j]) + ' ')
		file_SP_1.write('\n')
	file_SP_1.close()
	file_SP_0 = open('file_cycle_SP_0.txt', 'w')
	for i in range(SP_0.shape[0]):
		for j in range(SP_0.shape[1]):
			file_SP_0.write(str(SP_0[i][j]) + ' ')
		file_SP_0.write('\n')
	file_SP_0.close()
	"""

	# SP_distance: each FF's vector distance between label 1 and 0, shape(#FF)
	SP_distance = np.zeros((seq.shape[2]))
	for i in range(SP_distance.shape[0]):
		SP_distance[i] = np.linalg.norm(SP_1[:, i] - SP_0[:, i])

	# sort with index
	"""
	file_SP_distance = open('file_cycle_SP_distance.txt', 'w')
	for i in range(SP_distance.shape[0]):
		file_SP_distance.write(str(SP_distance[i]) + ' ')
	file_SP_distance.close()
	"""
	FF_index = np.argsort(-SP_distance)

	return FF_index[:n_FF_selected]


def FFSelect_sample(seq, targets, n_FF_selected):
	# input:
	# seq, targets, n_FF_selected
	# output:
	# indices of the selected FFs

	# SP: signal probabilities, shape(#sample, #FF)
	SP = np.zeros((seq.shape[0], seq.shape[2]))
	for i in range(seq.shape[0]):
		SP[i] = np.sum(seq[i], axis=0)

	SP = SP / seq.shape[0]

	file_SP = open('file_sample_SP.txt', 'w')
	for i in range(SP.shape[0]):
		for j in range(SP.shape[1]):
			file_SP.write(str(SP[i][j]) + ' ')
		file_SP.write('\n')
	file_SP.close()

	# SP_pearson, shape(#FF)
	SP_pearson = np.zeros((seq.shape[2]))
	for i in range(SP_pearson.shape[0]):
		SP_pearson[i], _ = stats.pearsonr(SP[:,i], targets)

	# sort with index
	file_SP_pearson = open('file_sample_SP_pearson.txt', 'w')
	for i in range(SP_pearson.shape[0]):
		file_SP_pearson.write(str(SP_pearson[i]) + ' ')
	file_SP_pearson.close()
	
	FF_index = np.argsort(-SP_pearson)

	return FF_index[:n_FF_selected]

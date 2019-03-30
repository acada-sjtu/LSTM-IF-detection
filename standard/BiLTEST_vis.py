import os
import sys
import numpy as np
import h5py
from sklearn.model_selection import train_test_split
from keras.models import Sequential, Model, model_from_json
from keras.layers import Input, LSTM, Dropout, Dense
from keras.layers import Bidirectional, concatenate
from keras.callbacks import ModelCheckpoint
from fileRead import file_read

# np.random.seed(0)

n_step = 50

file_path = sys.argv[1]
benchmark = file_path.split('_')[1]
pos = file_path.split('_')[2]

if file_path.split('_')[0]=='inputdata':
	faulty_label = 0
else:
	faulty_label = 1


# --------------------read data--------------------
seqTest, targetsTest = file_read(n_step, file_path, hasLabel=False, label=faulty_label)
if faulty_label:
	# affected for inputerror
	file_path2 = sys.argv[2]
	affected_raw = np.loadtxt(file_path2, dtype='int64').reshape(-1, n_step, seqTest.shape[2])
	affected = np.zeros((affected_raw.shape[0], n_step - 1, seqTest.shape[2]), dtype='int64')
	for i in range(affected.shape[0]):
		affected[i] = np.delete(affected_raw[i], 0, axis=0)


# --------------------load model--------------------
bilstm_model = model_from_json(open('models/bilstm_model_%s.json' % benchmark).read())
bilstm_model.load_weights("weights/bilstm_weights_%s.hdf5" % benchmark)
bi_hidden_states_model = model_from_json(open('models/bi_hidden_states_model_%s.json' % benchmark).read())
bi_hidden_states_model.load_weights("weights/bilstm_weights_%s.hdf5" % benchmark, by_name=True)



# --------------------evaluate--------------------
print 'evaluating...'
seq_num = xrange(len(seqTest))
A = 0
B = 0
C = 0
D = 0
if not os.path.exists('h_states'):
	os.mkdir('h_states')
if faulty_label:
	file_J = h5py.File('h_states/bi_hidden_states_J_%s_%s.hdf5' % (benchmark, pos), 'w')
else:
	file_J = h5py.File('h_states/bi_hidden_states_J_%s_free.hdf5' % benchmark, 'w')
file_J.create_group('input')
if faulty_label:
	file_J.create_group('affected')
file_J.create_group('bi_hidden_states')
file_J.create_group('rightORwrong')
print seqTest.shape
for test_num in seq_num:
	file_J['input'].create_dataset('input_%d'%test_num, data=seqTest[test_num])
	if faulty_label:
		file_J['affected'].create_dataset('affected_%d'%test_num, data=affected[test_num])
	prob = bilstm_model.predict(np.asarray([seqTest[test_num]]))
	guess = 1 if prob>=0.5 else 0
	bi_hidden_states = bi_hidden_states_model.predict(np.asarray([seqTest[test_num]]))
	file_J['bi_hidden_states'].create_dataset('bi_hidden_states_%d'%test_num, data=bi_hidden_states)
	if guess == 1:
		if targetsTest[test_num] == 1:
			D += 1
			file_J['rightORwrong'].create_dataset('rightORwrong_%d'%test_num, data=np.ones(1))
		else:
			C += 1
			file_J['rightORwrong'].create_dataset('rightORwrong_%d'%test_num, data=np.zeros(1))
	else:
		if targetsTest[test_num] == 1:
			B += 1
			file_J['rightORwrong'].create_dataset('rightORwrong_%d'%test_num, data=np.zeros(1))
		else:
			A += 1
			file_J['rightORwrong'].create_dataset('rightORwrong_%d'%test_num, data=np.ones(1))
	file_J.flush()
print('%10s%10s%10s' % (' ', 'True', 'False'))
print('%10s%10s%10s' % ('Positive', str(D), str(C)))
print('%10s%10s%10s' % ('Negative', str(A), str(B)))
precision = float(D)*100/(C+D)
recall = float(D)*100/(B+D)		
print 'precision: %.2f ' %precision
print 'recall: %.2f ' %	recall
file_J.close()
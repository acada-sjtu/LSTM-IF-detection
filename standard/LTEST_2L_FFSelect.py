import sys
import numpy as np
from sklearn.model_selection import train_test_split
from keras.models import Sequential, Model, model_from_json
from keras.layers import Input, LSTM, Dropout, Dense
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint
from fileRead import file_read

# np.random.seed(0)

n_step = 50

file_path = sys.argv[1]
benchmark = file_path.split('_')[0]


# --------------------read data--------------------
seqTest, targetsTest = file_read(n_step, file_path)


# --------------------FF selection--------------------
FF_index = np.load("FF_index.npy")
seqTest = seqTest[:, :, FF_index]


# --------------------load model--------------------
lstm_2l_model = model_from_json(open('models/lstm_2l_model_%s.json' % benchmark).read())
lstm_2l_model.load_weights("weights/lstm_2l_weights_%s.hdf5" % benchmark)


# --------------------evaluate--------------------
print 'evaluating...'
seq_num = xrange(len(seqTest))
A = 0
B = 0
C = 0
D = 0
print seqTest.shape
for test_num in seq_num:
	prob = lstm_2l_model.predict(np.asarray([seqTest[test_num]]))
	guess = 1 if prob>=0.5 else 0
	if guess == 1:
		if targetsTest[test_num] == 1:
			D += 1
		else:
			C += 1
	else:
		if targetsTest[test_num] == 1:
			B += 1
		else:
			A += 1
print '%10s%10s%10s' % (' ', 'True', 'False')
print '%10s%10s%10s' % ('Positive', str(D), str(C))
print '%10s%10s%10s' % ('Negative', str(A), str(B))
precision = float(D)*100/(C+D)
recall = float(D)*100/(B+D)     
print 'precision: %.2f ' % precision
print 'recall: %.2f ' % recall
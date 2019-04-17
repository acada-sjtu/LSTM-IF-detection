import os
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
n_epoch = 100
n_hidden = 1024

dropout_flag = 0
learning_rate = 0.01
decay_rate = learning_rate / n_epoch


# --------------------read data--------------------
if (len(sys.argv)==3):
	# 2 arguments
	file_path = sys.argv[1]
	file_path2 = sys.argv[2]
	benchmark = file_path.split('_')[0]
	seq, targets, seqTest, targetsTest = file_read(n_step, file_path, file_path2)
	print seq.shape, targets.shape
	print seqTest.shape, targetsTest.shape
	n_out = seq.shape[2]
else:
	# 1 argument
	file_path = sys.argv[1]
	benchmark = file_path.split('_')[1]
	seq, targets = file_read(n_step, file_path)
	seq, seqTest, targets, targetsTest = train_test_split(seq, targets, test_size=0.2)
	print seq.shape, targets.shape
	print seqTest.shape, targetsTest.shape
	n_out = seq.shape[2]


# --------------------construct model--------------------
# model = Sequential()
input_1 = Input(shape=(n_step-1, n_out), name='input_1')
h_states_1, state_h_1, state_c_1 = LSTM(n_hidden, activation='tanh', return_sequences=True, return_state=True)(input_1)
if dropout_flag:
	dropout_1 = Dropout(0.2)(state_h_1)
	dense_1 = Dense(1, activation='sigmoid', name='output_1')(dropout_1)
else:
	dense_1 = Dense(1, activation='sigmoid', name='output_1')(state_h_1)
# LSTM
lstm_model = Model(inputs=[input_1], outputs=[dense_1])
AdamOptimizer = Adam(lr=learning_rate, decay=decay_rate)
lstm_model.compile(optimizer=AdamOptimizer,
				   loss='binary_crossentropy',
				   metrics=['accuracy'])# hidden states
hidden_states_model = Model(inputs=[input_1], outputs=[h_states_1])


# --------------------save model--------------------
if not os.path.exists('models'):
	os.mkdir('models')
lstm_string = lstm_model.to_json()
open('models/lstm_model_%s.json'%benchmark, 'w').write(lstm_string)
hidden_states_string = hidden_states_model.to_json()
open('models/hidden_states_model_%s.json'%benchmark, 'w').write(hidden_states_string)


# --------------------training--------------------
if not os.path.exists('weights'):
	os.mkdir('weights')
checkpointer = ModelCheckpoint(filepath='weights/lstm_weights_%s.hdf5'%benchmark, verbose=1, save_best_only=True)
lstm_model.fit({'input_1': seq}, {'output_1': targets}, epochs=n_epoch, shuffle=True, batch_size=32, validation_data=(seqTest, targetsTest), callbacks=[checkpointer])
print lstm_model.evaluate(seqTest, targetsTest, batch_size=32)


# --------------------evaluate--------------------
print 'evaluating...'
seq_num = xrange(len(seqTest))
A = 0
B = 0
C = 0
D = 0
print seqTest.shape
for test_num in seq_num:
	prob = lstm_model.predict(np.asarray([seqTest[test_num]]))
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
print 'recall: %.2f ' %	recall

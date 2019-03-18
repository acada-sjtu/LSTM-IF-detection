import sys
import numpy as np
from sklearn.model_selection import train_test_split
from keras.models import Sequential, Model, model_from_json
from keras.layers import Input, Bidirectional, LSTM, Dropout, Dense
from keras.callbacks import ModelCheckpoint
from fileRead import file_read

# np.random.seed(0)

n_step = 50
n_epoch = 50
n_hidden = 16

lstm_dropout_flag = 0


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
bilstm_model = Sequential()
bilstm_model.add(Bidirectional(LSTM(n_hidden, return_sequences=False, activation='tanh'), input_shape=(n_steps-1, n_out)))
#model.add(Dropout(0.2))
bilstm_model.add(Dense(1,activation='sigmoid'))
bilstm_model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

   
# --------------------save model--------------------
lstm_string = lstm_model.to_json()
open('lstm_model_%s.json'%benchmark, 'w').write(lstm_string)


# --------------------training--------------------
checkpointer = ModelCheckpoint(filepath="bilstm_weights_%s.hdf5" % benchmark, verbose=1, save_best_only=True)
bilstm_model.fit(seq, targets, nb_epoch=epochs, shuffle=True, batch_size=32, validation_data=(seqTest, targetsTest), callbacks=[checkpointer])
print bilstm_model.evaluate(seqTest, targetsTest, batch_size=32)


# --------------------evaluate--------------------
seq_num = xrange(len(seqTest))
A = 0
B = 0
C = 0
D = 0
print seqTest.shape
for test_num in seq_num:
	guess = bilstm_model.predict_classes(np.asarray([seqTest[test_num]]))
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
print('%10s%10s%10s' % (' ', 'True', 'False'))
print('%10s%10s%10s' % ('Positive', str(D), str(C)))
print('%10s%10s%10s' % ('Negative', str(A), str(B)))
precision = float(D)*100/(C+D)
recall = float(D)*100/(B+D)		
print 'precision: %.2f ' %precision
print 'recall: %.2f ' %	recall
import sys
import numpy as np
import h5py
from sklearn.model_selection import train_test_split
from keras.models import Sequential, Model, model_from_json
from keras.layers import Input, LSTM, Dropout, Dense
from keras.callbacks import ModelCheckpoint
from fileRead import file_read

# np.random.seed(0)

n_step = 50

file_path = sys.argv[1]
benchmark = file_path.split('_')[0]


# --------------------read data--------------------
seqTest, targetsTest = file_read(n_steps, file_path)
# affected for inputerror
affected_raw = np.loadtxt(file_path3, dtype='int64').reshape(-1, n_steps, seqTest.shape[2])
affected = np.zeros((affected_raw.shape[0], n_steps - 1, seqTest.shape[2]), dtype='int64')
for i in range(affected.shape[0]):
    affected[i] = np.delete(affected_raw[i], 0, axis=0)


# --------------------load model--------------------
lstm_model = model_from_json(open('lstm_model_%s.json' % benchmark).read())
lstm_model.load_weights("lstm_weights_%s.hdf5" % benchmark)
hidden_states_model = model_from_json(open('hidden_states_model_%s.json' % benchmark).read())
hidden_states_model.load_weights("lstm_weights_%s.hdf5" % benchmark, by_name=True)


# --------------------evaluate--------------------
seq_num = xrange(len(seqTest))
A = 0
B = 0
C = 0
D = 0
file_J = h5py.File('hidden_states_J_free.hdf5', 'w')
file_J.create_group('input')
file_J.create_group('affected')
file_J.create_group('hidden_states')
file_J.create_group('rightORwrong')
print seqTest.shape
for test_num in seq_num:
    file_J['input'].create_dataset('input_%d'%test_num, data=seqTest[test_num])
    file_J['affected'].create_dataset('affected_%d'%test_num, data=affected[test_num])
    prob = lstm_model.predict(np.asarray([seqTest[test_num]]))
    guess = 1 if prob>=0.5 else 0
    hidden_states = hidden_states_model.predict(np.asarray([seqTest[test_num]]))
    file_J['hidden_states'].create_dataset('hidden_states_%d'%test_num, data=hidden_states)
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
print '%10s%10s%10s' % (' ', 'True', 'False')
print '%10s%10s%10s' % ('Positive', str(D), str(C))
print '%10s%10s%10s' % ('Negative', str(A), str(B))
precision = float(D)*100/(C+D)
recall = float(D)*100/(B+D)     
print 'precision: %.2f ' % precision
print 'recall: %.2f ' % recall
file_J.close()
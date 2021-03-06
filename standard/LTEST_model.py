import sys
import numpy as np
from sklearn.model_selection import train_test_split
from keras.models import Sequential, Model, model_from_json
from keras.layers import Input, LSTM, Dropout, Dense
from keras.callbacks import ModelCheckpoint
from fileRead import file_read

# np.random.seed(0)

n_step = 50

file_path = sys.argv[1]
benchmark = file_path.split('_')[0]

model_name = sys.argv[2]
weights_name = sys.argv[3]

if (len(sys.argv)==5 and sys.argv[4]=='1c'):
    config = tf.ConfigProto(intra_op_parallelism_threads=1,\
                            inter_op_parallelism_threads=1,\
                            device_count={'cpu':1, 'gpu':0})
    session = tf.Session(config=config)
    KTF.set_session(session)

    
# --------------------read data--------------------
seqTest, targetsTest = file_read(n_step, file_path)


# --------------------load model--------------------
lstm_model = model_from_json(open('lstm_model_%s.json' % benchmark).read())
lstm_model.load_weights("lstm_weights_%s.hdf5" % benchmark)


# --------------------evaluate--------------------
print 'evaluating...'
seq_num = xrange(len(seqTest))
A = 0
B = 0
C = 0
D = 0
print seqTest.shape
start = time.time()
for test_num in seq_num:
    guess = model.predict_classes(np.asarray([seqTest[test_num]]))
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
end = time.time()
print '%10s%10s%10s' % (' ', 'True', 'False')
print '%10s%10s%10s' % ('Positive', str(D), str(C))
print '%10s%10s%10s' % ('Negative', str(A), str(B))
precision = float(D)*100/(C+D)
recall = float(D)*100/(B+D)     
print 'precision: %.2f ' % precision
print 'recall: %.2f ' % recall

print "Inference ", seq_num, "samples: ", end-start
print "Average: ", (end-start)/seq_num


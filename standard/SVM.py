import os
import sys
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.externals import joblib
from sklearn.metrics import accuracy_score
from fileRead import file_read

# np.random.seed(0)

n_step = 50

file_path = sys.argv[1]
file_path2 = sys.argv[2]


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
seq_2d = np.reshape(seq, (seq.shape[0], -1))
seqTest_2d = np.reshape(seqTest, (seqTest.shape[0], -1))
print seq_2d.shape
print seqTest_2d.shape


#--------------------feature selection------------------'
# maybe FF selection, PCA, etc.


#--------------------construct model------------------
clf = svm.SVC(C=1.0, kernel='rbf')
# --------------------training--------------------
clf.fit(seq_2d, targets)
# --------------------save model--------------------
joblib.dump(clf, "svm_model.m")


# --------------------evaluate--------------------
print 'evaluating...'
seq_num = xrange(len(seqTest))
A = 0
B = 0
C = 0
D = 0
print seqTest.shape
for test_num in seq_num:
    guess = clf.predict(np.reshape(seqTest_2d[test_num], (1, -1)))[0]
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

print accuracy_score(targetsTest, clf.predict(seqTest_2d))
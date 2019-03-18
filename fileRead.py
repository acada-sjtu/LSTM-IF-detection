import numpy as np
def file_read(n_steps, file_path, file_path2='', hasLabel=True, label=0):
    """ Test RNN with binary outputs. """
    
    count = 0
    data_input = []
    seq = []
    targets= []
    seqTest = []
    targetsTest = []
    for l in open(file_path):
        if count == 0:
            count += 1
            targets.append(int(l))
            continue
        row = [int(x) for x in l.replace('\n','').split()]
        data_input.append(row)
        count += 1
        if (count == n_steps):
            count = 0
            seq.append(data_input[:])
            data_input = []
    
    seq = np.asarray(seq)
    targets = np.asarray(targets)
	
    if (file_path2==''):
        return (seq, targets)

#----------------test-------------------
    count = 0
    for l in open(file_path2):
        if count == 0:
            if hasLabel:
                targetsTest.append(int(l))
            count += 1
            continue
        row = [int(x) for x in l.replace('\n','').split()]
        data_input.append(row)
        count += 1
        if (count == n_steps):
            count = 0
            seqTest.append(data_input[:])
            if not hasLabel:
                # here to give label manually
                # 1 for faulty
                # 0 for fault-free
                targetsTest.append(label)
            data_input = []

    seqTest = np.asarray(seqTest)
    targetsTest = np.asarray(targetsTest)
    return (seq, targets, seqTest, targetsTest)

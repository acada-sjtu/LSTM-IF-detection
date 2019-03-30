import numpy as np
def file_read(n_steps, file_path, file_path2='', hasLabel=True, label=0):
    # if hasLabel=False, give label manually
    # 1 for faulty
    # 0 for fault-free
    # --------------------file 1--------------------
    seq = []
    targets= []
    seqTest = []
    targetsTest = []
    data_input = []
    count = 0
    for l in open(file_path):
        if count == 0:
            if hasLabel:
                targets.append(int(l))
            else:
                targets.append(label)
            count += 1
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


    # --------------------file 2--------------------
    count = 0
    for l in open(file_path2):
        if count == 0:
            if hasLabel:
                targetsTest.append(int(l))
            else:
                targetsTest.append(label)
            count += 1
            continue
        row = [int(x) for x in l.replace('\n','').split()]
        data_input.append(row)
        count += 1
        if (count == n_steps):
            count = 0
            seqTest.append(data_input[:])
            data_input = []

    seqTest = np.asarray(seqTest)
    targetsTest = np.asarray(targetsTest)
    return (seq, targets, seqTest, targetsTest)
# Make sure to check if the input has been included in the dataset
import sys
import random
CYCLE = 50
#INPUT_NUM = 32

filename1 = sys.argv[1]
filename2 = sys.argv[2]

benchmark = filename1.split('_')[1]
pos = filename1.split('_')[2]

count = 0
flag = 2
with open(filename1) as file_no, \
        open(filename2) as file_single,\
        open('dataset_%s_%s' % (benchmark, pos),'w+') as file_write:
    while 1:
        if not flag:
            break

        file_read = random.choice((file_single, file_no)) if flag==2 else file_read


        for i in xrange(CYCLE):
            line = file_read.readline()
            if not line :
                flag -= 1
                file_read = file_no if file_read is file_single else file_single
                break
            if count % CYCLE == 0:
                if file_read == file_no:
                    file_write.writelines('0\n')
                else:
                    file_write.writelines('1\n')
                count += 1
                continue

            file_write.writelines(item + ' ' for item in line.split()[:]) #slice input here
            file_write.writelines('\n')
            count += 1

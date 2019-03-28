import sys
CYCLE = 50
filename1 = sys.argv[1]
filename2 = sys.argv[2]
ff_num = int(sys.argv[3])
file1 = open(filename1)
file2 = open(filename2)
ff_sign=[]
for j in range(ff_num):
    ff_sign.append(0)
for i in range(2000*CYCLE):
    num_list_1 = file1.readline().split()
    num_list_2 = file2.readline().split()
    for ff in range(ff_num):
        if num_list_1[ff] != num_list_2[ff]:
            #print ff-input_num
            ff_sign[ff] += 1
index_list = []
for index,item in enumerate(ff_sign):
	if item>CYCLE:
		index_list.append(index)
	else:
		print index


file1.close()
file2.close()


print ff_sign
print len(index_list)
for filename  in [filename2, filename1]:
    fileopen = open(filename)
    filewrite = open(filename+'-c','w+')
    while 1:
        
        line_c = ''
        line  = fileopen.readline()
        if not line:# or test>10:
            break
        value_wire = line.split()
        for ff_num in index_list:
            line_c += str(value_wire[ff_num])+' '
        line_c += '\n'
        filewrite.writelines(line_c)
    fileopen.close()
    filewrite.close()

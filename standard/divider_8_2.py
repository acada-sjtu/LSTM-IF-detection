import sys

filename = sys.argv[1]
benchmark = filename.split('_')[1]
pos = filename.split('_')[-1]

file_tr = '%s_train_%s_0.8' % (benchmark, pos)
file_te = '%s_test_%s_0.2' % (benchmark, pos)


line_num = len(open(filename, 'r').readlines())
print line_num
cnt = 0

with open(filename) as file,\
	open(file_tr,'w+') as file_tr,\
		open(file_te,'w+') as file_te:

	for line in file:
		if cnt<0.8*line_num or cnt>=1.0*line_num:
			file_tr.writelines(line)
		else:
			file_te.writelines(line)
		cnt += 1


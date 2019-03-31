benchmark = '_or1200_synth_'
benchmark = '_leon3mp_synth_'

file_inputdata_new = open('inputdata' + benchmark + 'f', 'w')
for i in range(1, 8):
	file_inputdata = open('inputdata' + benchmark + str(i) + '_f', 'r')
	for line in file_inputdata:
		file_inputdata_new.write(line)

file_inputerror_new = open('inputerror' + benchmark + 'f', 'w')
for i in range(1, 8):
	file_inputerror = open('inputerror' + benchmark + str(i) + '_f', 'r')
	for line in file_inputerror:
		file_inputerror_new.write(line)

file_affected_new = open('affected' + benchmark + 'f', 'w')
for i in range(1, 8):
	file_affected = open('affected' + benchmark + str(i) + '_f', 'r')
	for line in file_affected:
		file_affected_new.write(line)



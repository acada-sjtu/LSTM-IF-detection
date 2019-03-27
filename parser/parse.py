import sys

filename = sys.argv[1]
print('Parsing', filename, '...')
file = open(filename, 'r')
file_new = open(filename.split('.')[0] + '.bench', 'w')

one_line = 0
line_cache = ''
io_cand = []
input_array = []
output_array = []
wire_array = []
operator_set = set([])
operation_array = []


class Operation:
	# init
	def __init__(self, op):
		self.operator = op
		self.input_node = []
		self.output_node = ''
	# print
	def show(self):
		print('Operator:', self.operator)
		print('Input nodes:', self.input_node)
		print('Output node:', self.output_node)


def parseMultiBit(line): # input/output for multi-bit
	end = line.find(']')
	sub_2, sub_1 = line[1:end].split(':')
	io_name = line[end+1:].strip(' ;')
	io_array = []
	for i in range(int(sub_1), int(sub_2)+1):
		io_array.append(io_name + '[' + str(i) + ']')
	return io_array


def parseSingleBit(line): # input/output for single-bit
	io_array = line.strip(' ;').split(',')
	for i in range(len(io_array)):
		io_array[i] = io_array[i].strip()
	return io_array


def parseNode(key_word, line):
	global io_cand
	global input_array
	global output_array
	global wire_array
	# module
	if (key_word == 'module'):
		beg = line.find('(')
		end = line.rfind(')')
		line = line[beg+1:end]
		io_cand = line.split(',')
		for i in range(len(io_cand)):
			io_cand[i] = io_cand[i].strip()
	# input
	elif (key_word == 'input'):
		line = line[5:].strip()
		if (line[0] == '['): # input [19:0] pic_ints_i;
			input_array_tmp = parseMultiBit(line)
			input_array = input_array + input_array_tmp
			io_cand.remove(input_array_tmp[0].split('[')[0])
		else:
			input_array_tmp = parseSingleBit(line)
			input_array = input_array + input_array_tmp
			for input_1 in input_array_tmp:
				io_cand.remove(input_1)
	# output
	elif (key_word == 'output'):
		line = line[6:].strip()
		if (line[0] == '['): # output [31:0] iwb_adr_o;
			output_array_tmp = parseMultiBit(line)
			output_array = output_array + output_array_tmp
			io_cand.remove(output_array_tmp[0].split('[')[0])
		else:
			output_array_tmp = parseSingleBit(line)
			output_array = output_array + output_array_tmp
			for output_1 in output_array_tmp:
				io_cand.remove(output_1)
	# wire
	elif (key_word == 'wire'):
		line = line[4:].strip()
		if (line[0] == '['):
			wire_array_tmp = parseMultiBit(line)
			wire_array = wire_array + wire_array_tmp
		else:
			wire_array_tmp = parseSingleBit(line)
			wire_array  = wire_array + wire_array_tmp
	else:
		raise('Exception')


def parseOperation(op, line):
	operator_set.add(key_word)
	# -----parse IO array-----
	io_array = line[line.find('(')+1 : line.rfind(')')].split(',')
	for i in range(len(io_array)):
		io_tmp = io_array[i]
		io_array[i] = io_tmp[io_tmp.find('(')+1 : io_tmp.find(')')]
	# -----parse operator-----
	if (op[:3] == 'AND'):
		print(op)
		exit()
	elif (op[:2] == 'OR'):
		if (op not in ['OR2x2_ASAP7_75t_SL']):
			print(line)
			exit()
		operation = Operation('OR')
		input_num = int(op[2])
		for i in range(input_num):
			operation.input_node.append(io_array[i])
		operation.output_node = io_array[-1]
		operation_array.append(operation)
	elif (op[:3] == 'INV'):
		if (op not in ['INVx1_ASAP7_75t_SL']):
			print(line)
			exit()
		operation = Operation('NOT')
		operation.input_node.append(io_array[0])
		operation.output_node = io_array[-1]
	elif (op[:6] == 'A2O1A1'):
		print(line)
		exit()
	# protential ob
	elif (op[:3] == 'DFF'):
		if (op not in ['DFFHQNx1_ASAP7_75t_SL']):
			print(line)
			exit()
		operation = Operation('DFF')
		operation.input_node.append(io_array[0])
		operation.output_node = io_array[-1]
	elif (op[:9] == 'ASYNC_DFF'): # TODO: uncertain logic
		if (op not in ['ASYNC_DFFHx1_ASAP7_75t_SL']):
			print(line)
			exit()
		operation = Operation('ASYNC_DFF')
		operation.input_node.append(io_array[0])
		operation.output_node = io_array[-1]
	else:
		print(op)
		exit()



# main
for line in file:
	line = line.strip()
	if (line == ''):
		continue
	line_cache = line_cache + line
	if (line[-1] != ';'):
		continue
	else:
		key_word = line_cache.split(' ')[0]
		# ----------moduel, input, output, wire----------
		if (key_word=='module' or key_word=='input' or key_word=='output' or key_word=='wire'):
			parseNode(key_word, line_cache)
		# ----------operations----------
		else:
			# print(key_word)
			parseOperation(key_word, line_cache)
			# print(line_cache[:20])
			# print('TODO')
			# exit()
		# empty line_cache
		line_cache = ''
# write bench
file_new.write('input ')
for node in input_array:
	if (node == input_array[-1]):
		file_new.write(node + ';')
	else:
		file_new.write(node + ',')
file_new.write('\n\n')
file_new.write('output ')
for node in output_array:
	if (node == output_array[-1]):
		file_new.write(node + ';')
	else:
		file_new.write(node + ',')









file.close()
file_new.close()


# calculation
AND_operator_array = []
OR_operator_array = []
INV_operator_array = []
XOR_operator_array = []
XNOR_operator_array = []
NAND_operator_array = []
NOR_operator_array = []
AO_operator_array = []
OA_operator_array = []
AnOn_operator_array = []
OnAn_operator_array = []
MAJ_operator_array = []
# potential ob
BUF_operator_array = []
DFF_operator_array = []
ADFF_operator_array = []
# others
TIE_operator_array = []

un_operator_array = list(operator_set)
un_operator_array.sort()

for op in un_operator_array:
	if (op[:3] == 'AND'):
		AND_operator_array.append(op)
	elif (op[:2] == 'OR'):
		OR_operator_array.append(op)
	elif (op[:3] == 'INV'):
		INV_operator_array.append(op)
	elif (op[:3] == 'XOR'):
		XOR_operator_array.append(op)
	elif (op[:4] == 'XNOR'):
		XNOR_operator_array.append(op)
	elif (op[:4] == 'NAND'):
		NAND_operator_array.append(op)
	elif (op[:3] == 'NOR'):
		NOR_operator_array.append(op)
	elif (op[:2] == 'AO'):
		AO_operator_array.append(op)
	elif (op[:2] == 'OA'):
		OA_operator_array.append(op)
	elif (op[:6] == 'A2O1A1'):
		AnOn_operator_array.append(op)
	elif (op[:6] == 'O2A1O1'):
		OnAn_operator_array.append(op)
	elif (op[:3] == 'MAJ'):
		MAJ_operator_array.append(op)
	# potential ob
	elif (op[:3] == 'BUF'):
		BUF_operator_array.append(op)
	elif (op[:3] == 'DFF'):
		DFF_operator_array.append(op)
	elif (op[:9] == 'ASYNC_DFF'):
		ADFF_operator_array.append(op)
	# others
	elif (op[:3] == 'TIE'):
		TIE_operator_array.append(op)


for op in AND_operator_array:
	un_operator_array.remove(op)
for op in OR_operator_array:
	un_operator_array.remove(op)
for op in INV_operator_array:
	un_operator_array.remove(op)
for op in XOR_operator_array:
	un_operator_array.remove(op)
for op in XNOR_operator_array:
	un_operator_array.remove(op)
for op in NAND_operator_array:
	un_operator_array.remove(op)
for op in NOR_operator_array:
	un_operator_array.remove(op)
for op in AO_operator_array:
	un_operator_array.remove(op)
for op in OA_operator_array:
	un_operator_array.remove(op)
for op in AnOn_operator_array:
	un_operator_array.remove(op)
for op in OnAn_operator_array:
	un_operator_array.remove(op)
for op in MAJ_operator_array:
	un_operator_array.remove(op)
for op in BUF_operator_array:
	un_operator_array.remove(op)
for op in DFF_operator_array:
	un_operator_array.remove(op)
for op in ADFF_operator_array:
	un_operator_array.remove(op)
for op in TIE_operator_array:
	un_operator_array.remove(op)



print('%-2d AND operators' % len(AND_operator_array))
print('%-2d OR operators' % len(OR_operator_array))
print('%-2d INV operators' % len(INV_operator_array))
print('%-2d XOR operators' % len(XOR_operator_array))
print('%-2d XNOR operators' % len(XNOR_operator_array))
print('%-2d NAND operators' % len(NAND_operator_array))
print('%-2d NOR operators' % len(NOR_operator_array))
print('%-2d AO operators' % len(AO_operator_array))
print('%-2d OA operators' % len(OA_operator_array))
print('%-2d AnOn operators' % len(AnOn_operator_array))
print('%-2d OnAn operators' % len(OnAn_operator_array))
print('%-2d MAJ operators' % len(MAJ_operator_array))
print('%-2d BUF operators' % len(BUF_operator_array))
print('%-2d DFF operators' % len(DFF_operator_array))
print('%-2d ADFF operators' % len(ADFF_operator_array))
print('%-2d TIE operators' % len(TIE_operator_array))
print('%-2d unknown operators, which are:' % len(un_operator_array))

for op in un_operator_array:
	print('      ', op)
		
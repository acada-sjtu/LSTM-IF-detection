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

# tmp nodes
class tmpNode:
	# class variable
	cnt = 0
	# init
	def __init__(self):
		tmpNode.cnt = tmpNode.cnt + 1

	def getNode(self):
		return 'tmp' + str(tmpNode.cnt)


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
	# ----------parse IO array----------
	io_array = line[line.find('(')+1 : line.rfind(')')].split(',')
	for i in range(len(io_array)):
		io_tmp = io_array[i]
		io_array[i] = io_tmp[io_tmp.find('(')+1 : io_tmp.find(')')]
	# ----------parse operator----------
	# AND -> AND
	if (op[:3] == 'AND'):
		if (op not in ['AND2x2_ASAP7_75t_SL', 'AND2x2_ASAP7_75t_SRAM', 'AND2x4_ASAP7_75t_SL',
					   'AND2x6_ASAP7_75t_SL', 'AND3x4_ASAP7_75t_SL', 'AND4x1_ASAP7_75t_SL',
					   'AND3x1_ASAP7_75t_SL', 'AND3x2_ASAP7_75t_SL', 'AND3x1_ASAP7_75t_SRAM']):
			print('NOT FOUND')
			print(op)
			print(line)
			print(io_array)
			exit()
		operation = Operation('AND')
		param = int(op[3])
		operation.input_node = io_array[:param]
		operation.output_node = io_array[-1]
		operation_array.append(operation)
	# OR -> OR
	elif (op[:2] == 'OR'):
		if (op not in ['OR2x2_ASAP7_75t_SL', 'OR2x6_ASAP7_75t_SL', 'OR3x2_ASAP7_75t_SL', 'OR2x4_ASAP7_75t_SL',
					   'OR3x1_ASAP7_75t_SL', 'OR4x1_ASAP7_75t_SL', 'OR3x4_ASAP7_75t_SL', 'OR3x1_ASAP7_75t_SRAM']):
			print('NOT FOUND')
			print(op)
			print(line)
			print(io_array)
			exit()
		operation = Operation('OR')
		param = int(op[2])
		operation.input_node = io_array[:param]
		operation.output_node = io_array[-1]
		operation_array.append(operation)
	# NAND -> NAND
	elif (op[:4] == 'NAND'):
		if (op not in ['NAND2x1_ASAP7_75t_SL', 'NAND2x1p5_ASAP7_75t_SL', 'NAND2x2_ASAP7_75t_SL',
					   'NAND2xp5_ASAP7_75t_SL', 'NAND2xp5_ASAP7_75t_SRAM', 'NAND2xp33_ASAP7_75t_SL',
					   'NAND2xp33_ASAP7_75t_SRAM', 'NAND2xp67_ASAP7_75t_SL', 'NAND3x1_ASAP7_75t_SL',
					   'NAND3xp33_ASAP7_75t_SL', 'NAND4xp25_ASAP7_75t_SL', 'NAND3x2_ASAP7_75t_SL',
					   'NAND2xp67_ASAP7_75t_SRAM', 'NAND4xp75_ASAP7_75t_SL', 'NAND3xp33_ASAP7_75t_SRAM',
					   'NAND4xp25_ASAP7_75t_SRAM', 'NAND2x1p5_ASAP7_75t_SRAM', 'NAND2x1_ASAP7_75t_SRAM',
					   'NAND2x2_ASAP7_75t_SRAM']):
			print('NOT FOUND')
			print(op)
			print(line)
			print(io_array)
			exit()
		operation = Operation('NAND')
		param = int(op[4])
		operation.input_node = io_array[:param]
		operation.output_node = io_array[-1]
		operation_array.append(operation)
	# NOR -> NOR
	elif (op[:3] == 'NOR'):
		if (op not in ['NOR2x1_ASAP7_75t_SL', 'NOR2x1p5_ASAP7_75t_SL', 'NOR2x2_ASAP7_75t_SL',
					   'NOR2xp33_ASAP7_75t_SL', 'NOR2xp67_ASAP7_75t_SL', 'NOR3xp33_ASAP7_75t_SL',
					   'NOR4xp75_ASAP7_75t_SL', 'NOR3x1_ASAP7_75t_SL', 'NOR2xp33_ASAP7_75t_SRAM',
					   'NOR3xp33_ASAP7_75t_SRAM', 'NOR4xp25_ASAP7_75t_SL', 'NOR4xp25_ASAP7_75t_SRAM',
					   'NOR2xp67_ASAP7_75t_SRAM']):
			print('NOT FOUND')
			print(op)
			print(line)
			print(io_array)
			exit()
		operation = Operation('NOR')
		param = int(op[3])
		operation.input_node = io_array[:param]
		operation.output_node = io_array[-1]
		operation_array.append(operation)
	# INV -> NOT
	elif (op[:3] == 'INV'):
		if (op not in ['INVx1_ASAP7_75t_SL', 'INVx2_ASAP7_75t_SL', 'INVx3_ASAP7_75t_SL', 'INVx4_ASAP7_75t_SL',
					   'INVx5_ASAP7_75t_SL', 'INVx6_ASAP7_75t_SL', 'INVx8_ASAP7_75t_SL', 'INVxp33_ASAP7_75t_SRAM',
					   'INVxp33_ASAP7_75t_SL', 'INVxp67_ASAP7_75t_SL', 'INVx13_ASAP7_75t_SL', 'INVx11_ASAP7_75t_SL',
					   'INVxp67_ASAP7_75t_SRAM', 'INVx4_ASAP7_75t_SRAM', 'INVx1_ASAP7_75t_SRAM']):
			print('NOT FOUND')
			print(op)
			print(line)
			print(io_array)
			exit()
		operation = Operation('NOT')
		operation.input_node = [io_array[0]]
		operation.output_node = io_array[-1]
		operation_array.append(operation)
	# XOR -> XOR
	elif (op[:3] == 'XOR'):
		if (op not in ['XOR2x1_ASAP7_75t_SL', 'XOR2x2_ASAP7_75t_SL', 'XOR2xp5_ASAP7_75t_SL']):
			print('NOT FOUND')
			print(op)
			print(line)
			print(io_array)
			exit()
		operation = Operation('XOR')
		param = int(op[3])
		operation.input_node = io_array[:param]
		operation.output_node = io_array[-1]
		operation_array.append(operation)
	# XNOR -> XNOR
	elif (op[:4] == 'XNOR'):
		if (op not in ['XNOR2x1_ASAP7_75t_SL', 'XNOR2x2_ASAP7_75t_SL', 'XNOR2xp5_ASAP7_75t_SL',
					   'XNOR2xp5_ASAP7_75t_SRAM']):
			print('NOT FOUND')
			print(op)
			print(line)
			print(io_array)
			exit()
		operation = Operation('XNOR')
		param = int(op[4])
		operation.input_node = io_array[:param]
		operation.output_node = io_array[-1]
		operation_array.append(operation)
	# AO / AOI -> AND + OR / NOR
	elif (op[:2] == 'AO'):
		if (op not in ['AOI21xp5_ASAP7_75t_SL', 'AOI22xp5_ASAP7_75t_SL', 'AOI31xp67_ASAP7_75t_SL',
					   'AOI22x1_ASAP7_75t_SL', 'AOI21x1_ASAP7_75t_SL', 'AOI211x1_ASAP7_75t_SL',
					   'AO21x2_ASAP7_75t_SL', 'AO21x1_ASAP7_75t_SL', 'AOI21xp33_ASAP7_75t_SL',
					   'AOI31xp33_ASAP7_75t_SL', 'AOI22xp33_ASAP7_75t_SRAM', 'AOI211xp5_ASAP7_75t_SL',
					   'AOI21xp33_ASAP7_75t_SRAM', 'AO31x2_ASAP7_75t_SL', 'AO22x1_ASAP7_75t_SL',
					   'AOI22xp33_ASAP7_75t_SL', 'AOI211xp5_ASAP7_75t_SRAM', 'AO21x1_ASAP7_75t_SRAM',
					   'AOI31xp33_ASAP7_75t_SRAM', 'AO211x2_ASAP7_75t_SL', 'AOI222xp33_ASAP7_75t_SL',
					   'AOI21xp5_ASAP7_75t_SRAM']):
			print('NOT FOUND')
			print(op)
			print(line)
			print(io_array)
			exit()
		# print(line)
		if (op[2] == 'I'):
			params = op[3 : op.find('x')]
		else:
			params = op[2 : op.find('x')]
		input_ = []
		p = 0
		for param_c in params:
			param = int(param_c)
			if (param != 1):
				operation = Operation('AND')
				operation.input_node = io_array[p : p + param]
				node = tmpNode().getNode()
				operation.output_node = node
				# operation.show()
				operation_array.append(operation)
				input_.append(node)
				p += param
			else:
				input_.append(io_array[p])
				p += 1
		if (op[2] == 'I'):
			operation = Operation('NOR')
		else:
			operation = Operation('OR')
		operation.input_node = input_
		operation.output_node = io_array[-1]
		# operation.show()
		operation_array.append(operation)
		# if (op == 'AOI222xp33_ASAP7_75t_SL'):
			# exit()
	# OA / OAI -> OR + AND / NAND
	elif (op[:2] == 'OA'):
		if (op not in ['OAI21xp33_ASAP7_75t_SL', 'OAI31xp33_ASAP7_75t_SRAM', 'OAI21xp5_ASAP7_75t_SL',
					   'OAI22xp5_ASAP7_75t_SL', 'OAI21x1_ASAP7_75t_SL', 'OAI22x1_ASAP7_75t_SL',
					   'OA21x2_ASAP7_75t_SL', 'OAI211xp5_ASAP7_75t_SL', 'OAI22xp33_ASAP7_75t_SRAM',
					   'OAI21xp33_ASAP7_75t_SRAM', 'OAI22xp33_ASAP7_75t_SL', 'OAI31xp33_ASAP7_75t_SL',
					   'OA22x2_ASAP7_75t_SL', 'OAI211xp5_ASAP7_75t_SRAM', 'OA21x2_ASAP7_75t_SRAM',
					   'OA211x2_ASAP7_75t_SL', 'OAI222xp33_ASAP7_75t_SL', 'OAI321xp33_ASAP7_75t_SL']):
			print('NOT FOUND')
			print(op)
			print(line)
			print(io_array)
			exit()
		# print(line)
		if (op[2] == 'I'):
			params = op[3 : op.find('x')]
		else:
			params = op[2 : op.find('x')]
		input_ = []
		p = 0
		for param_c in params:
			param = int(param_c)
			if (param != 1):
				operation = Operation('OR')
				operation.input_node = io_array[p : p + param]
				node = tmpNode().getNode()
				operation.output_node = node
				# operation.show()
				operation_array.append(operation)
				input_.append(node)
				p += param
			else:
				input_.append(io_array[p])
				p += 1
		if (op[2] == 'I'):
			operation = Operation('NAND')
		else:
			operation = Operation('AND')
		operation.input_node = input_
		operation.output_node = io_array[-1]
		# operation.show()
		operation_array.append(operation)
		# if (op == 'OAI222xp33_ASAP7_75t_SL'):
			# exit()
	# A2O1A1I -> AND + OR + NAND,  A2O1A1O1I -> AND + OR + AND + NOR
	elif (op[:2] == 'A2'):
		if (op not in ['A2O1A1Ixp33_ASAP7_75t_SL', 'A2O1A1O1Ixp25_ASAP7_75t_SL', 'A2O1A1Ixp33_ASAP7_75t_SRAM']):
			print('NOT FOUND')
			print(op)
			print(line)
			print(io_array)
			exit()
		# A2 -> AND
		operation_1 = Operation('AND')
		operation_1.input_node = io_array[:2]
		node_1 = tmpNode().getNode()
		operation_1.output_node = node_1
		operation_array.append(operation_1)
		if (op[2:4] == 'O1'):
			# O1 -> OR
			operation_2 = Operation('OR')
			operation_2.input_node = [node_1, io_array[2]]
			node_2 = tmpNode().getNode()
			operation_2.output_node = node_2
			operation_array.append(operation_2)
			if (op[4:6] == 'A1'):
				if (op[6] == 'I'):
					# A1I -> NAND
					operation_3 = Operation('NAND')
					operation_3.input_node = [node_2, io_array[3]]
					operation_3.output_node = io_array[-1]
					operation_array.append(operation_3)
				else:
					# A1 -> AND
					operation_3 = Operation('AND')
					operation_3.input_node = [node_2, io_array[3]]
					node_3 = tmpNode().getNode()
					operation_3.output_node = node_3
					operation_array.append(operation_3)
					if (op[6:8] == 'O1'):
						if (op[8] == 'I'):
							# O1I -> NOR
							operation_4 = Operation('NOR')
							operation_4.input_node = [node_3, io_array[4]]
							operation_4.output_node = io_array[-1]
							operation_array.append(operation_4)
						else:
							raise('Exception')
					else:
						raise('Exception')
			else:
				raise('Exception')
		else:
			raise('Exception')
	# O2A1O1I -> OR + AND + NOR
	elif (op[:2] == 'O2'):
		if (op not in ['O2A1O1Ixp5_ASAP7_75t_SL', 'O2A1O1Ixp33_ASAP7_75t_SL', 'O2A1O1Ixp33_ASAP7_75t_SRAM',
					   'O2A1O1Ixp5_ASAP7_75t_SRAM']):
			print('NOT FOUND')
			print(op)
			print(line)
			print(io_array)
			exit()
		# O2 -> OR
		operation_1 = Operation('OR')
		operation_1.input_node = io_array[:2]
		node_1 = tmpNode().getNode()
		operation_1.output_node = node_1
		operation_array.append(operation_1)
		if (op[2:4] == 'A1'):
			# A1 -> AND
			operation_2 = Operation('AND')
			operation_2.input_node = [node_1, io_array[2]]
			node_2 = tmpNode().getNode()
			operation_2.output_node = node_2
			operation_array.append(operation_2)
			if (op[4:6] == 'O1'):
				if (op[6] == 'I'):
					# O1I -> NOR
					operation_3 = Operation('NOR')
					operation_3.input_node = [node_2, io_array[3]]
					operation_3.output_node = io_array[-1]
					operation_array.append(operation_3)
				else:
					raise('Exception')
			else:
				raise('Exception')
		else:
			raise('Exception')
	# MAJ / MAJI -> OR / NOR (AND1, AND2, AND3)
	elif (op[:3] == 'MAJ'):
		if (op not in ['MAJIxp5_ASAP7_75t_SL', 'MAJx2_ASAP7_75t_SL', 'MAJx3_ASAP7_75t_SL']):
			print('NOT FOUND')
			print(op)
			print(line)
			print(io_array)
			exit()
		# AND1
		operation_1 = Operation('AND')
		operation_1.input_node = [io_array[0], io_array[1]]
		node_1 = tmpNode().getNode()
		operation_1.output_node = node_1
		operation_array.append(operation_1)
		# AND2
		operation_2 = Operation('AND')
		operation_2.input_node = [io_array[0], io_array[2]]
		node_2 = tmpNode().getNode()
		operation_2.output_node = node_2
		operation_array.append(operation_2)
		# AND3
		operation_3 = Operation('AND')
		operation_3.input_node = [io_array[1], io_array[2]]
		node_3 = tmpNode().getNode()
		operation_3.output_node = node_3
		operation_array.append(operation_3)
		# OR / NOR
		if (op[3] == 'I'): # NOR
			operation_4 = Operation('NOR')
		else: # OR
			operation_4 = Operation('OR')
		operation_4.input_node = [node_1, node_2, node_3]
		operation_4.output_node = io_array[-1]
		operation_array.append(operation_4)
	# -----others-----
	elif (op[:5] == 'TIEHI'):
		if (op not in ['TIEHIx1_ASAP7_75t_SL']):
			print('NOT FOUND')
			print(op)
			print(line)
			print(io_array)
			exit()
		operation = Operation('TIEHI')
		operation.input_node = []
		operation.output_node = io_array[-1]
		operation_array.append(operation)
	elif (op[:5] == 'TIELO'):
		if (op not in ['TIELOx1_ASAP7_75t_SL']):
			print('NOT FOUND')
			print(op)
			print(line)
			print(io_array)
			exit()
		operation = Operation('TIELO')
		operation.input_node = []
		operation.output_node = io_array[-1]
		operation_array.append(operation)
	elif (op[:2] == 'FA'): # TODO: uncertain logic=======================================================================
		if (op not in ['FAx1_ASAP7_75t_SL']):
			print('NOT FOUND')
			print(op)
			print(line)
			print(io_array)
			exit()
		return
	elif (op[:2] == 'HA'): # TODO: uncertain logic=======================================================================
		if (op not in ['HAxp5_ASAP7_75t_SL']):
			print('NOT FOUND')
			print(op)
			print(line)
			print(io_array)
			exit()
		return
	elif (op[:2] == 'HB'): # TODO: uncertain logic=======================================================================
		if (op not in ['HB1xp67_ASAP7_75t_SL']):
			print('NOT FOUND')
			print(op)
			print(line)
			print(io_array)
			exit()
		return
	elif (op[:4] == 'SDFH'): # TODO: uncertain logic=======================================================================
		if (op not in ['SDFHx4_ASAP7_75t_SL', 'SDFHx1_ASAP7_75t_SL', 'SDFHx1_ASAP7_75t_SRAM']):
			print('NOT FOUND')
			print(op)
			print(line)
			print(io_array)
			exit()
		return
	# -----protential ob-----
	# DFF -> DFF
	elif (op[:3] == 'DFF'): # TODO: uncertain logic=====================================================================
		if (op not in ['DFFHQNx1_ASAP7_75t_SL', 'DFFHQNx1_ASAP7_75t_SRAM', 'DFFHQNx2_ASAP7_75t_SL',\
					   'DFFHQNx3_ASAP7_75t_SL', 'DFFHQNx2_ASAP7_75t_SRAM', 'DFFHQx4_ASAP7_75t_SL']):
			print('NOT FOUND')
			print(op)
			print(line)
			print(io_array)
			exit()
		operation = Operation('DFF')
		operation.input_node = [io_array[0]]
		operation.output_node = io_array[-1]
		operation_array.append(operation)
	# ASYNC_DFF -> ASYNC_DFF
	elif (op[:9] == 'ASYNC_DFF'): # TODO: uncertain logic===============================================================
		if (op not in ['ASYNC_DFFHx1_ASAP7_75t_SL', 'ASYNC_DFFHx1_ASAP7_75t_SRAM']):
			print('NOT FOUND')
			print(op)
			print(line)
			print(io_array)
			exit()
		operation = Operation('DFF')
		operation.input_node = [io_array[0]]
		operation.output_node = io_array[-1]
		operation_array.append(operation)
	# BUF -> DFF
	elif (op[:3] == 'BUF'):
		if (op not in ['BUFx2_ASAP7_75t_SL', 'BUFx3_ASAP7_75t_SL', 'BUFx5_ASAP7_75t_SL', 'BUFx6f_ASAP7_75t_SL',
					   'BUFx4_ASAP7_75t_SL', 'BUFx4f_ASAP7_75t_SL', 'BUFx12f_ASAP7_75t_SL', 'BUFx16f_ASAP7_75t_SL',
					   'BUFx10_ASAP7_75t_SL', 'BUFx8_ASAP7_75t_SL']):
			print('NOT FOUND')
			print(op)
			print(line)
			print(io_array)
			exit()
		operation = Operation('DFF')
		operation.input_node = [io_array[0]]
		operation.output_node = io_array[-1]
		operation_array.append(operation)
	elif (op == 'spram'): # TODO: uncertain logic=======================================================================
		return
	elif (op == 'tpram'): # TODO: uncertain logic=======================================================================
		return
	else:
		print(op)
		print(line)
		print(io_array)
		exit()



# --------------------read verilog--------------------
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
		# ----------operation----------
		else:
			operator_set.add(key_word)
			parseOperation(key_word, line_cache)
			# print(line_cache[:20])
			# print('TODO')
			# exit()
		# empty line_cache
		line_cache = ''
file.close()
# --------------------write bench--------------------
file_new.write('input ')
for node in input_array:
	if (node == input_array[-1]):
		file_new.write(node + ';\n')
	else:
		file_new.write(node + ',')
file_new.write('\n')
file_new.write('output ')
for node in output_array:
	if (node == output_array[-1]):
		file_new.write(node + ';\n')
	else:
		file_new.write(node + ',')
file_new.write('\n')
for operation in operation_array:
	file_new.write(operation.output_node + ' = ')
	file_new.write(operation.operator + '(')
	for node in operation.input_node:
		if (node == operation.input_node[-1]):
			file_new.write(node + ')\n')
		else:
			file_new.write(node + ', ')
file_new.close()




# calculation
AND_operator_array = []
OR_operator_array = []
NAND_operator_array = []
NOR_operator_array = []
INV_operator_array = []
XOR_operator_array = []
XNOR_operator_array = []
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
	elif (op[:4] == 'NAND'):
		NAND_operator_array.append(op)
	elif (op[:3] == 'NOR'):
		NOR_operator_array.append(op)
	elif (op[:3] == 'INV'):
		INV_operator_array.append(op)
	elif (op[:3] == 'XOR'):
		XOR_operator_array.append(op)
	elif (op[:4] == 'XNOR'):
		XNOR_operator_array.append(op)
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
for op in NAND_operator_array:
	un_operator_array.remove(op)
for op in NOR_operator_array:
	un_operator_array.remove(op)
for op in INV_operator_array:
	un_operator_array.remove(op)
for op in XOR_operator_array:
	un_operator_array.remove(op)
for op in XNOR_operator_array:
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
print('%-2d NAND operators' % len(NAND_operator_array))
print('%-2d NOR operators' % len(NOR_operator_array))
print('%-2d INV operators' % len(INV_operator_array))
print('%-2d XOR operators' % len(XOR_operator_array))
print('%-2d XNOR operators' % len(XNOR_operator_array))
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
		
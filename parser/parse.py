import sys

filename = sys.argv[1]
print('Parsing', filename, '...')
file = open(filename, 'r')
file_new = open(filename.split('.')[0] + '.bench', 'w')

line_cache = ''

io_cand = []
input_array = []
output_array = []
wire_array = []
build_output_dic_flag = 0
output_dic = {} # check the existence of outputs' logic modules

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


def stripAll(array):
	for i in range(len(array)):
		array[i] = array[i].strip()
	return array


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
	io_array = stripAll(io_array)
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
		io_cand = stripAll(io_cand)
	# input
	elif (key_word == 'input'):
		line = line[5:].strip()
		if (line[0] == '['): # input [19:0] pic_ints_i;
			input_array_tmp = parseMultiBit(line)
			input_array += input_array_tmp
			io_cand.remove(input_array_tmp[0].split('[')[0])
		else:
			input_array_tmp = parseSingleBit(line)
			input_array += input_array_tmp
			for input_1 in input_array_tmp:
				io_cand.remove(input_1)
	# output
	elif (key_word == 'output'):
		line = line[6:].strip()
		if (line[0] == '['): # output [31:0] iwb_adr_o;
			output_array_tmp = parseMultiBit(line)
			output_array += output_array_tmp
			io_cand.remove(output_array_tmp[0].split('[')[0])
		else:
			output_array_tmp = parseSingleBit(line)
			output_array += output_array_tmp
			for output_1 in output_array_tmp:
				io_cand.remove(output_1)

	# wire
	elif (key_word == 'wire'):
		line = line[4:].strip()
		if (line[0] == '['):
			wire_array_tmp = parseMultiBit(line)
			wire_array += wire_array_tmp
		else:
			wire_array_tmp = parseSingleBit(line)
			wire_array += wire_array_tmp
	else:
		raise('Exception')


def parseOperation(op, line):
	global input_array
	# ----------parse IO array----------
	io_array_tmp = line[line.find('(')+1 : line.rfind(')')].split('.')
	io_array_tmp = stripAll(io_array_tmp)
	io_array = []
	for io_tmp in io_array_tmp:
		if (io_tmp == ''):
			continue
		io = io_tmp[io_tmp.find('(')+1 : io_tmp.rfind(')')]
		io_array.append(io)
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
		if (operation.output_node in output_array):
			output_dic[operation.output_node] = 1
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
		if (operation.output_node in output_array):
			output_dic[operation.output_node] = 1
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
		if (operation.output_node in output_array):
			output_dic[operation.output_node] = 1
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
		if (operation.output_node in output_array):
			output_dic[operation.output_node] = 1
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
		if (operation.output_node in output_array):
			output_dic[operation.output_node] = 1
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
		if (operation.output_node in output_array):
			output_dic[operation.output_node] = 1
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
		if (operation.output_node in output_array):
			output_dic[operation.output_node] = 1
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
		if (op[2] == 'I'):
			params = op[3 : op.find('x')]
		else:
			params = op[2 : op.find('x')]
		input_ = []
		p = 0
		for param_char in params:
			param = int(param_char)
			if (param != 1):
				operation = Operation('AND')
				operation.input_node = io_array[p : p + param]
				node = tmpNode().getNode()
				operation.output_node = node
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
		operation_array.append(operation)
		if (operation.output_node in output_array):
			output_dic[operation.output_node] = 1
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
		if (op[2] == 'I'):
			params = op[3 : op.find('x')]
		else:
			params = op[2 : op.find('x')]
		input_ = []
		p = 0
		for param_char in params:
			param = int(param_char)
			if (param != 1):
				operation = Operation('OR')
				operation.input_node = io_array[p : p + param]
				node = tmpNode().getNode()
				operation.output_node = node
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
		operation_array.append(operation)
		if (operation.output_node in output_array):
			output_dic[operation.output_node] = 1
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
					if (operation_3.output_node in output_array):
						output_dic[operation_3.output_node] = 1
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
							if (operation_4.output_node in output_array):
								output_dic[operation_4.output_node] = 1
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
					if (operation_3.output_node in output_array):
						output_dic[operation_3.output_node] = 1
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
		if (operation_4.output_node in output_array):
			output_dic[operation_4.output_node] = 1
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
		if (operation.output_node in output_array):
			output_dic[operation.output_node] = 1
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
		if (operation.output_node in output_array):
			output_dic[operation.output_node] = 1
	elif (op[:2] == 'FA'):
		if (op not in ['FAx1_ASAP7_75t_SL']):
			print('NOT FOUND')
			print(op)
			print(line)
			print(io_array)
			exit()
		# FAx1_ASAP7_75t_SL ( .A(), .B(), .CI(), .CON(), .SN() );
		# operation 1
		operation_1 = Operation('NOT')
		operation_1.input_node = [io_array[0]]
		node_1 = tmpNode().getNode()
		operation_1.output_node = node_1 # A_bar
		operation_array.append(operation_1)
		# operation 2
		operation_2 = Operation('NOT')
		operation_2.input_node = [io_array[1]]
		node_2 = tmpNode().getNode()
		operation_2.output_node = node_2 # B_bar
		operation_array.append(operation_2)
		# operation 3
		operation_3 = Operation('NOT')
		operation_3.input_node = [io_array[2]]
		node_3 = tmpNode().getNode()
		operation_3.output_node = node_3 # CI_bar
		operation_array.append(operation_3)
		# --calculate CON--
		if (io_array[-2] != ''):
			# operation 4
			operation_4 = Operation('AND')
			operation_4.input_node = [node_1, node_2]
			node_4 = tmpNode().getNode()
			operation_4.output_node = node_4
			operation_array.append(operation_4)
			# operation 5
			operation_5 = Operation('AND')
			operation_5.input_node = [node_1, node_3]
			node_5 = tmpNode().getNode()
			operation_5.output_node = node_5
			operation_array.append(operation_5)
			# operation 6
			operation_6 = Operation('AND')
			operation_6.input_node = [node_2, node_3]
			node_6 = tmpNode().getNode()
			operation_6.output_node = node_6
			operation_array.append(operation_6)
			# operation 7
			operation_7 = Operation('OR')
			operation_7.input_node = [node_4, node_5, node_6]
			operation_7.output_node = io_array[-2] # CON
			operation_array.append(operation_7)
			if (operation_7.output_node in output_array):
				output_dic[operation_7.output_node] = 1
		# --calculate SN--
		if (io_array[-1] != ''):
			# operation 8
			operation_8 = Operation('AND')
			operation_8.input_node = [node_1, node_2, node_3]
			node_8 = tmpNode().getNode()
			operation_8.output_node = node_8
			operation_array.append(operation_8)
			# operation 9
			operation_9 = Operation('AND')
			operation_9.input_node = [node_1, io_array[1], io_array[2]]
			node_9 = tmpNode().getNode()
			operation_9.output_node = node_9
			operation_array.append(operation_9)
			# operation 10
			operation_10 = Operation('AND')
			operation_10.input_node = [io_array[0], node_2, io_array[2]]
			node_10 = tmpNode().getNode()
			operation_10.output_node = node_10
			operation_array.append(operation_10)
			# operation 11
			operation_11 = Operation('AND')
			operation_11.input_node = [io_array[0], io_array[1], node_3]
			node_11 = tmpNode().getNode()
			operation_11.output_node = node_11
			operation_array.append(operation_11)
			# operation 12
			operation_12 = Operation('OR')
			operation_12.input_node = [node_8, node_9, node_10, node_11]
			operation_12.output_node = io_array[-1] # SN
			operation_array.append(operation_12)
			if (operation_12.output_node in output_array):
				output_dic[operation_12.output_node] = 1
	elif (op[:2] == 'HA'):
		if (op not in ['HAxp5_ASAP7_75t_SL']):
			print('NOT FOUND')
			print(op)
			print(line)
			print(io_array)
			exit()
		# HAxp5_ASAP7_75t_SL ( .A(), .B(), .CON(), .SN() );
		# operation 1
		operation_1 = Operation('NOT')
		operation_1.input_node = [io_array[0]]
		node_1 = tmpNode().getNode()
		operation_1.output_node = node_1 # A_bar
		operation_array.append(operation_1)
		# operation 2
		operation_2 = Operation('NOT')
		operation_2.input_node = [io_array[1]]
		node_2 = tmpNode().getNode()
		operation_2.output_node = node_2 # B_bar
		operation_array.append(operation_2)
		# --calculate CON--
		if (io_array[-2] != ''):
			# operation 3
			operation_3 = Operation('OR')
			operation_3.input_node = [node_1, node_2]
			operation_3.output_node = io_array[-2] # CON
			operation_array.append(operation_3)
			if (operation_3.output_node in output_array):
				output_dic[operation_3.output_node] = 1
		# --calculate SN--
		if (io_array[-1] != ''):
			# operation 4
			operation_4 = Operation('AND')
			operation_4.input_node = [node_1, node_2]
			node_4 = tmpNode().getNode()
			operation_4.output_node = node_4
			operation_array.append(operation_4)
			# operation 5
			operation_5 = Operation('AND')
			operation_5.input_node = io_array[:2]
			node_5 = tmpNode().getNode()
			operation_5.output_node = node_5
			operation_array.append(operation_5)
			# operation 6
			operation_6 = Operation('OR')
			operation_6.input_node = [node_4, node_5]
			operation_6.output_node = io_array[-1] # SN
			operation_array.append(operation_6)
			if (operation_6.output_node in output_array):
				output_dic[operation_6.output_node] = 1
	elif (op[:2] == 'HB'):
		if (op not in ['HB1xp67_ASAP7_75t_SL']):
			print('NOT FOUND')
			print(op)
			print(line)
			print(io_array)
			exit()
		# HB1xp67_ASAP7_75t_SL ( .A(), .Y() );
		operation = Operation('DFF')
		operation.input_node = [io_array[0]]
		operation.output_node = io_array[-1]
		operation_array.append(operation)
		if (operation.output_node in output_array):
			output_dic[operation.output_node] = 1
	elif (op == 'spram'):
		"""
		When simulating BENCH files, the .q in spram have no input.
		Therefore, I parse them as inputs.
		"""
		# spram ( .clock(), .ce(), .wren(), .address(), .data(), .q() );
		interface_array = io_array[-1].strip('{}').split(',') # .q
		interface_array = stripAll(interface_array)
		input_array_tmp = []
		for interface in interface_array:
			for wire in wire_array:
				if (wire == interface):
					input_array_tmp.append(wire)
				elif (wire.find(interface) >= 0):
					if (wire[wire.find(interface)+len(interface)] == '['):
						input_array_tmp.append(wire)
		input_array += input_array_tmp
	elif (op == 'tpram'):
		"""
		When simulating BENCH files, the [.do_a .do_b] in tpram have no input.
		Therefore, I parse them as inputs.
		"""
		# tpram ( .clock(), .rst(), .ce_a(), .addr_a(), .do_a(), .ce_b(), .addr_b(), .do_b(), .ce_w(), .we_w(), .addr_w(), .di_w() );
		interface_array_1 = io_array[4].strip('{}').split(',') # .do_a
		interface_array_2 = io_array[7].strip('{}').split(',') # .do_b
		interface_array = interface_array_1 + interface_array_2
		interface_array = stripAll(interface_array)
		input_array_tmp = []
		for interface in interface_array:
			for wire in wire_array:
				if (wire == interface):
					input_array_tmp.append(wire)
				elif (wire.find(interface) >= 0):
					if (wire[wire.find(interface)+len(interface)] == '['):
						input_array_tmp.append(wire)
		input_array += input_array_tmp
	# -----protential ob-----
	# DFF -> DFF
	elif (op[:3] == 'DFF'):
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
		if (operation.output_node in output_array):
			output_dic[operation.output_node] = 1
	# ASYNC_DFF -> ASYNC_DFF
	elif (op[:9] == 'ASYNC_DFF'):
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
		if (operation.output_node in output_array):
			output_dic[operation.output_node] = 1
	elif (op[:4] == 'SDFH'):
		if (op not in ['SDFHx4_ASAP7_75t_SL', 'SDFHx1_ASAP7_75t_SL', 'SDFHx1_ASAP7_75t_SRAM']):
			print('NOT FOUND')
			print(op)
			print(line)
			print(io_array)
			exit()
		# SDFHx4_ASAP7_75t_SL ( .D(), .SI(), .SE(), .CLK(), .QN() );
		# operation 1
		operation_1 = Operation('NOT')
		operation_1.input_node = [io_array[2]]
		node_1 = tmpNode().getNode()
		operation_1.output_node = node_1
		operation_array.append(operation_1)
		# operation 2
		operation_2 = Operation('AND')
		operation_2.input_node = [io_array[0], node_1]
		node_2 = tmpNode().getNode()
		operation_2.output_node = node_2
		operation_array.append(operation_2)
		# operation 3
		operation_3 = Operation('AND')
		operation_3.input_node = io_array[1:3]
		node_3 = tmpNode().getNode()
		operation_3.output_node = node_3
		operation_array.append(operation_3)
		# operation 4
		operation_4 = Operation('OR')
		operation_4.input_node = [node_2, node_3]
		node_4 = tmpNode().getNode()
		operation_4.output_node = node_4
		operation_array.append(operation_4)
		# operation 5
		operation_5 = Operation('DFF')
		operation_5.input_node = [node_4]
		operation_5.output_node = io_array[-1] # QN
		operation_array.append(operation_5)
		if (operation_5.output_node in output_array):
			output_dic[operation_5.output_node] = 1
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
		if (operation.output_node in output_array):
			output_dic[operation.output_node] = 1
	else:
		raise('Unknown operator.')


# --------------------read Verilog--------------------
while True:
	line = file.readline()
	if not line:
		break
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
			# build dic for output_array
			if (not build_output_dic_flag):
				for output in output_array:
					output_dic[output] = 0
				build_output_dic_flag = 1
			operator_set.add(key_word)
			parseOperation(key_word, line_cache)
			# print(line_cache[:20])
			# print('TODO')
			# exit()
		# empty line_cache
		line_cache = ''
file.close()
# remove the redundant outputs
for k, v in output_dic.items():
	if (v == 0):
		output_array.remove(k)
# --------------------write BENCH--------------------
file_new.write('input ')
for i in range(len(input_array)):
	if (i == len(input_array)-1):
		file_new.write(input_array[i])
	else:
		file_new.write(input_array[i] + ',')
file_new.write(';\n\n')
file_new.write('output ')
for i in range(len(output_array)):
	if (i == len(output_array)-1):
		file_new.write(output_array[i])
	else:
		file_new.write(output_array[i] + ',')
file_new.write(';\n\n')
for operation in operation_array:
	file_new.write(operation.output_node)
	file_new.write(' = ')
	file_new.write(operation.operator)
	file_new.write('(')
	for i in range(len(operation.input_node)):
		if (i == len(operation.input_node)-1):
			file_new.write(operation.input_node[i])
		else:
			file_new.write(operation.input_node[i] + ', ')
	file_new.write(')\n')
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

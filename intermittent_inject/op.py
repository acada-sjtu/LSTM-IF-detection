from boardError import *

class Op:
	"""
	Here is the class that embodies the logic operators
	"""

	def __init__(self, which, operands):
		self.operands = operands
		self.which = which
		self.last = 0
		self.value = 0
		self.visited = False
		
	def reset(self):
		self.value = 0
		self.last = 0
		
	def calc(self, valOperands):
		"""
		This calculates the result of which(operands).
		"""
		if self.which == "AND":
			res = valOperands[0]
			for valOperand in valOperands[1:]:
				res = res & valOperand
			self.value = res
		elif self.which == "NAND":
			res = valOperands[0]
			for valOperand in valOperands[1:]:
				res = res & valOperand
			self.value = int(not res)
		elif self.which == "OR":
			res = valOperands[0]
			for valOperand in valOperands[1:]:
				res = res | valOperand
			self.value = res
		elif self.which == "NOR":
			res = valOperands[0]
			for valOperand in valOperands[1:]:
				res = res | valOperand
			self.value =  int(not res)
		elif self.which == "XOR":
			res = valOperands[0]
			for valOperand in valOperands[1:]:
				res = res ^ valOperand
			self.value = res
		elif self.which == "XNOR":
			res = valOperands[0]
			for valOperand in valOperands[1:]:
				res = res ^ valOperand
			self.value = int(not res)
		elif self.which == "NOT":
			self.value  = int(not valOperands[0])
		elif self.which == "DFF":
			#print("len = ", len(valOperands))
			self.value = self.last
			self.last = int(valOperands[0])
			#return int(valOperands[0])
		else:
			raise BoardError("wrong operator ( " + self.which + " )")
		return self.value

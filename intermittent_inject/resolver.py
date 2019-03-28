from board import *
import os

class Resolver:
	
	def __init__(self, board):
		"""
		Some nodes are re-used multiple times when calculating several outputs.
		Since each node is unique and holds a unique value, it could save some time to remember it.
		However, all that is remembered gotta be wiped out as soon as one parameter has changed.
		"""
		self.board = board
		self.remembering = {"inValues":"none", "error":"none", "modifier":"none"}
		self.remembered = {}
		
	def resolve(self, inValues, error = "", modifier = ""):
		"""
		This takes the input values as a parameter and returns the output from the associated board.
		"""
		outValues = {}

		for op in self.board.ops.values():
			op.visited = False
                        
		for op in self.board.ops.keys():
			self.solve(op, inValues, error, modifier)

		for output in self.board.outputs:
			outValues[output] = self.solve(output, inValues, error, modifier)

		return outValues
			
	def regsolve(self, reg, inValues, error = "", modifier = ""):
		regValues = self.solve(reg, inValues, error, modifier)
		return regValues
	
	def reset(self):
		for op in self.board.ops.values():
			op.reset()

	def solve(self, node, inValues, error = "", modifier = ""):

		"""
		This functions takes a node as a parameter and returns its value.
		"""
		
		#print("visited " +node)
		#Test the memory validity
		if self.remembering["inValues"] != inValues or self.remembering["error"] != error or self.remembering["modifier"] != modifier:
			self.remembered = {}
			self.remembering["inValues"] = inValues
			self.remembering["error"] = error
			self.remembering["modifier"] = modifier
		#print("node is: ",node)	
		if node in self.board.inputs:
			return inValues[node]
		else:
			op = self.board.ops[node]
			if op.visited:
				return op.value
			op.visited = True
			valOperands = []
			
			#print("operands-len = ",len(op.operands))
			#print(op.operands)
			
			#input()
			for operand in op.operands:
				valOperands.append(self.solve(operand, inValues, error, modifier))
			#print("calculated ", node, valOperands)
			if self.board.isFlawed:
				# print op.operands
				op.value = op.calc(valOperands, error, modifier)
			else:
				op.value = op.calc(valOperands)
			#print("result of ", node, "is", op.value)
			return op.value

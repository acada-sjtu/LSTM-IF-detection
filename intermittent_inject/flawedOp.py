from op import *

class FlawedOp(Op):
	"""
	This class takes the output of a classic Op but flaws it accordingly to the supervisor.
	"""
	count = 0
	
	def __init__(self, which, operands):
		Op.__init__(self, which, operands)
		self.number = FlawedOp.count
		FlawedOp.count += 1
	
	
	def calc(self, valOperands, error, modifier):
		res = Op.calc(self, valOperands)
		# print("result:",res,"\n")
		
		e = int(error[self.number])
		# print("self.number:",e,"\n")
		if e == 0:
			# print("right result:", res,"\n")
			return res
		elif modifier == "01":
			# print("fault result: 1\n")
			return 1
		else:
			# print("fault result: 0\n")
			# print valOperands
			return 0

		# out = e ^ res
		# sel = str(int(modifier[0]) & e)
		# sel += str(int(modifier[1]) & e)
		# if sel == "01":
		# 	return 1
		# elif sel == "10":
		# 	return 0
		# else:
		# 	return out

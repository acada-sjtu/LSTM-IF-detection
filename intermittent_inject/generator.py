import math
import random

class Generator:
	"""
	This generates from a number N of bits all the possible combinations.
	It also generates from a number k all combinations of N-vector with k bits at 1.
	"""
	
	
	def __init__(self, N):
		self.N = N
		self.nodes = ["init"]
		self.vector = ""
 
	def next(self):
		"""
		Returns the next vector in the list of all combinations for a N-bit vector.
		"""
		#last iteration
		if len(self.nodes) == 0:
			return "Done"
			
		#first iteration
		if self.nodes[0] == "init":
			self.nodes = []
			for i in range(self.N):
				self.nodes.append(i)
				self.vector += "0"
			#print("self.vector=",self.vector)
			return self.vector
			
		#now we're gonna go up to the last registered node to change and shift the corresponding bit
		#the left bits will be set at 0 and their position registered as a node
		floor = self.nodes[len(self.nodes)-1]
		self.vector = self.vector[:floor] + "1"
		self.nodes.pop()
		while len(self.vector) < self.N:
			self.vector += "0"
			self.nodes.append(len(self.vector)-1)
		#print("self.vector=",self.vector)
		return self.vector

	def dec2bin(self,num,N):
		mid = []
		while True:
			if N == 0: break
			N -= 1
			num,rem = divmod(num,2)
			mid.append(rem)

		return ''.join([str(x) for x in mid[:]])
	
	def randomNext(self):
		randomnum = random.randrange(0,2**self.N,1)
		self.vector = self.dec2bin(randomnum,self.N)

		return self.vector

	def randomError(self, k=0, i=0):
		if k == 0:
			self.errorVector = self.dec2bin(0,self.N)
		elif k == 1:
			randomnum = random.randrange(0,self.N,1)
			self.errorVector = self.dec2bin(2**i,self.N)

		else:
			randomnum = random.randrange(0,2**self.N,1)
			self.errorVector = self.dec2bin(randomnum,self.N)
			
		#print (self.errorVector)
		return self.errorVector

	def randomError_supervised(self, reg_num):
		num = reg_num
		self.errorVector = self.dec2bin(2**num)
		
	def nextOfK(self, k):
		"""
		Returns the next vector in the list of all combinations for a N-bit vector with k bits at 1.
		"""
		#print ("k = ", k)
		v = self.next()
		#print ("v = ", v)
		#print ("count = ", v.count('1'))
		if v == "Done" or v.count('1') == k:
			return v
		else:
			return self.nextOfK(k)
			
	def reset(self):
		"""
		As the class keep tracks on which vectors have already been returned, when all have been computed through, there's nothing more to be done.
		To get a new set of the combinations, one must either re-instantiate this class or use this reset function.
		"""
		self.nodes = ["init"]
		self.vector = ""

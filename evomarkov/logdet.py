import numpy as np
from collections import Counter
import math 

class LogDet:
	def __init__(self, alphabet):
		self.index = {e: i for i, e in  enumerate(alphabet)}
		self.N = len(alphabet)
		self.cache = dict()
		self.verbose = False
		self.J12 = np.zeros((self.N, self.N))
		self.absJ = True
	def __call__(self, a, b, tag=None):
		return self.evaluate(a, b, tag)

	def evaluate(self, s1, s2, tag=None):
		#print(tag)
		self.J12.fill(0)   # = np.zeros((N, N))
		assert len(s1) == len(s2)
		for k, v in Counter(zip(s1, s2)).items():
			a1, a2 = k[0], k[1]
			x, y = self.index[a1] , self.index[a2]
			self.J12[x][y] = v
		if self.verbose: print(self.J12)
		D1 = np.diag(self.J12.sum(axis=1))
		D2 = np.diag(self.J12.sum(axis=0))
		d1 = np.linalg.det(D1)
		d2 = np.linalg.det(D2)
		J = np.linalg.det(self.J12)
		
		if J <= 0:
			print('#warn J<=0', J, tag)
			if self.verbose: print([d1, d2, J, self.J12, tag])
			if not self.absJ:
				return None
			else:
				J = -J
		if not ( d1 != 0 and d2 != 0 and J != 0):
			raise Exception([tag, [d1, d2, J,  self.J12]])
		d =  -np.log(J / np.sqrt(d1*d2))
		assert d >= 0 and not math.isnan(d), [d1, d2, J, d, self.J12, tag]
		return d





def dmatrix(data):
	def __states(d):
		states = set()
		for e in d.values():
			states.update(e)
		return sorted(list(states))

	hashed = dict()
	states = __states(data)

	lm = LogDet(states)
	for a in data:
		hashed[a] = dict()
		for b in data:
			if a == b: hashed[a][b] = 0
			elif a in hashed.get(b, {}):
				hashed[a][b] = hashed[b][a]
			else:
				hashed[a][b] = lm(data[a], data[b], (a, b))
	
	return hashed, states






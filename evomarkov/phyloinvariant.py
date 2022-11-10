import numpy as np
import itertools as it
from pyext import ext #import ext
# follow section 2: https://arxiv.org/pdf/1712.01719.pdf


def test_all3x3minors(n, M=None):
	minors, dets = list(), list()
	if False:
		a = np.arange(n*n).reshape(n, n)
		m = n
	else:
		(n, m) = M.shape
		a = M
		print(M.shape)

	for rows in it.combinations(list(range(n)), 3):
		for columns in it.combinations(list(range(m)), 3):
			e = a[np.ix_(rows, columns)]
			dets.append(np.linalg.det(e))
			#print(dets[-1])
			minors.append(e)
	return (minors, a, dets)

class PhyloInvariant:
	@staticmethod
	def vectorized2bdist(h, leaves):
		n = len(leaves)
		nv = ext.uniq([len(h[e]) for e in leaves]) 
		data = dict()
		for i in range(nv):
			tensor = [h[l][i] for l in leaves]
			for e in tensor: assert e == 0 or e == 1
			k = tuple(tensor)
			if not k in data: data[k] = 0
			data[k] = data[k] + 1
		bdist = {k: float(data[k])/nv for k in data}
		return {'leaves': leaves, 'bdist' : bdist}
		

	def all3x3minors(self, a, rows, cols, nonzeros):
		s = sum(a[x, y] for (x,y) in nonzeros) 
		assert s >= 0.9999 and s <= 1.0001, [a, s]
		#print('#nonzeros', s)
		for (x, y) in nonzeros:
			assert a[x, y] > 0
		(x, y)  = a.shape
		for i in range(x):
			for j in range(y):
				if not (i, j) in nonzeros:
					assert a[i, j] == 0, a
				else:
					assert a[i, j] > 0
		


		dets, minors = list(), list()
		if self.verbose: print('#log', [rows, cols])
		rows = list(range(x))
		cols = list(range(y))
		for rset in it.combinations(rows, 3):
			for cset in it.combinations(cols, 3):
				e = a[np.ix_(rset, cset)]
				dets.append(np.linalg.det(e))
				minors.append((rset, cset))
		return dets, minors


	def to_index(self, u):
		#print(u)
		for e in u:
			assert e == 0 or e == 1
		return int(sum(e * 2**i for i, e in enumerate(u))) 
	
	def __init__(self, leaves, bdist):
		try:
			n = int(leaves)
			self.leaves = [e for e in range(n)]
		except:
			assert isinstance(leaves, list)
			self.leaves = leaves
			n = len(leaves) #set(list(range(n)))
		
		self.dist = bdist
		self.N = 2**n
		self.n = n
		assert len(set(bdist)) == len(bdist)
		for e in bdist:
			assert len(e) == n
		self.verbose = False

	def flattening_matrix(self, a, b):
		a = set(a)
		assert set(list(a) + b) == set(self.leaves) and len(set(a).intersection(b)) == 0, [a, b, self.leaves]
		adist, bdist = list(), list()
		rows, cols, nonzeros = set(), set(),list()
		m = np.zeros(shape=(2**len(a), 2**len(b)))
		#ti = self.to_index([1 for e in range(3)])
		#assert ti == 7, ti
		for e in self.dist:
			x = self.to_index([e[i] for i, l in enumerate(self.leaves) if l in a])
			y = self.to_index([e[i] for i, l in enumerate(self.leaves) if not l in a])
			if self.dist[e] != 0:
				#print(e, self.dist[e], x,  y)
				m[x, y] = self.dist[e]
				rows.add(x)
				cols.add(y)
				nonzeros.append((x, y))
			else:
				assert self.dist[e] == 0

		return (m, rows, cols, nonzeros)



def testphylo():
	bdist =  {
		(0,0,0) : 0.0,
		(0,0,1) : 0.1,
		(0,1,0) : 0.2,
		(0,1,1) : 0.3,
		(1,0,0) : 0.4,
		(1,0,1) : 0.5,
		(1,1,0) : 0.6,
		(1,1,1) : 0.7,
	}
	
	phylo = PhyloInvariant(3, bdist)
	u, v = [0, 1], [2]
	(m, x, y,nz) = phylo.flattening_matrix(u, v)
	print(m)
	print(x,y, u, v, nz)

def testphylo1():
	(minors, m, dets) = test_all3x3minors(5)
	for e in minors:
		print(e)
	print(m)

def testphylo3():
	(minors, m, dets) = test_all3x3minors(64)
	print(max(dets))

def testphylo2():
	bdist =  {
        (1, 0,0,0) : 1,
        (1, 0,0,1) : 1,
        (1, 0,1,0) : 1,
        (0, 1,0,0) : 1,
        (1, 1,0,1) : 1,
        (1, 1,1,0) : 1,
    	(0, 1,1,1) : 1,
		(0,0,0,0) : 1,
	}

	phylo = PhyloInvariant(4, bdist)
	u, v = [0, 1], [2, 3]
	(m, x, y,nz) = phylo.flattening_matrix(u, v)
	print(m)
	print(x,y, u, v, nz)
	(dets, minors)= phylo.all3x3minors(m, x, y,nz)
	m = max(dets)
	mi = dets.index(m)
	print(m, minors[mi] )



if __name__ == '__main__':
	testphylo3()

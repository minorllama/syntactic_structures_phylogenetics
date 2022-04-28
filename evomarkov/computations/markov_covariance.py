from sympy import *
from pyext import Json
init_printing(use_unicode=True)


import itertools as it

def transition_m(name):
	s00, s11 = symbols("{0}00 {0}11".format(name))
	return Matrix([[s00, 1-s00], [1-s11, s11]])

def edge_covariance(v, m, u=None):
	if not u: u = v*m
	mv = 0 * v[0] + 1 * v[1]
	mu = 0 * u[0] + 1 * u[1]
	return v[1]*m[1,1]  - mv*mu

def bernoulli_variance(v):
	return v[1]*v[0]

p = Matrix([[0.5, 0.5]])
mR = transition_m("R")
mA = transition_m("A")
mC = transition_m("C")
mB = transition_m("B")
mE = transition_m("E")


def binary(x):
	if isinstance(x, list) or isinstance(x, tuple):
		return ["{0}={0:b}".format(e) for e in x]
	else:
		return "{0}={0:b}".format(x) 


def covariance():
	cov = dict()
	cov["rc"] = edge_covariance(p, mR * mC)
	cov["ra"] = edge_covariance(p, mR * mE * mA)
	cov["rb"] = edge_covariance(p, mR * mE * mB)
	cov["ab"] = bernoulli_variance(p * mR * mE)
	cov["ac"] = bernoulli_variance(p * mR)
	cov["bc"] = bernoulli_variance(p * mR)
	return cov

def p_flat(p,r,c,a,b):
	def p_flat_internal(r,c,a,b, e1, e2):
		e1_given_r = mR[r, e1]
		c_given_e1 = mC[e1, c]
		e2_given_e1 = mE[e1, e2]
		a_given_e2 = mA[e2, a]
		b_given_e2 = mB[e2, b]
		return    b_given_e2 * a_given_e2 * e2_given_e1 * c_given_e1 * e1_given_r

	pr = p[r]
	prob = 0
	for e1 in [0, 1]:
		for e2 in [0, 1]:
			prob += p_flat_internal(r,c,a,b, e1, e2) * pr

	return prob		

	#pc = (mR*mC)[r, c]
	#pa = (mR*mE*mA)[r, a]
	#pb = (mR*mE*mB)[r, b]
	#return pr * pa * pc * pb

def flattening(initial, check = False):
	hashed = Matrix([[0]*4]*4)
	labels = Matrix([[0]*4]*4)
	seen = set()
	for iR, iC in [(0, 0), (0, 1), (1,0), (1, 1)]:
		for iA, iB in [(0, 0), (0, 1), (1,0), (1, 1)]:
			x, y = 2*iR + iC, 2*iA + iB
			hashed[x, y] = p_flat(initial, iR, iC, iA, iB)
			l = 'p{0}{1}{2}{3}'.format(iR, iC, iA, iB)  
			assert not l in seen
			seen.add(l)
			l = symbols(l)
			labels[x, y] = l 
	# check all 3x3 minors vanish
	if not check: return hashed, labels
	for i in range(4):
		for j in range(4):
			mij = expand(hashed.minor(i, j))
			assert mij == 0, [i, j, mij]
			print("minor", i, j, mij)
	return hashed, labels



def test_covariance_quotients(flat, labels, verbose=True):
	def test_exact_quotient(f, g):
		f = Poly(f)
		g = Poly(g)
		try: return f.exquo(g)
		except Exception as e: return None

	cov = covariance()


# m = Matrix([[4*x+y for y in range(4)] for x in range(4) ])
# >>> m
# >>> Matrix([
# >>> [ 0,  1,  2,  3],
# >>> [ 4,  5,  6,  7],
# >>> [ 8,  9, 10, 11],
# >>> [12, 13, 14, 15]])
# rs = [0,1]
# cs = [2,3]
# Matrix([[m[j, i] for i in cs] for j in rs])
# >>> Matrix([
# >>> [2, 3],
# >>> [6, 7]])

	for row_select in it.combinations([0, 1, 2, 3], 2):
		for col_select in it.combinations([0, 1, 2, 3], 2): 
			m = Matrix([[flat[j, i] for i in col_select] for j in row_select])
			labelled = Matrix([[labels[j, i] for i in col_select] for j in row_select])
			det = expand(m.det())
			row_s = binary(row_select)
			col_s = binary(col_select)
			if det == 0:
				if verbose: print("skipped:minor_vanishes", (row_s, col_s), det)
			else:
				if verbose: print("minor_does_not_vanish", (row_s, col_s), labelled.det())
				
				nodivisor = True
				for k in cov:
					quotient = test_exact_quotient(det, cov[k]) 
					if quotient:
						nodivisor = False
						fac = factor(quotient)
						print('#', (row_select, col_select), k, fac, labelled.det())
				if nodivisor:
					print('#__nodivisors__', labelled.det())
				


flat, labels = flattening(p)
print(flat)
test_covariance_quotients(flat, labels)
print(labels)














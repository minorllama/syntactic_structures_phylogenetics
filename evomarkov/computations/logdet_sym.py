from sympy import Matrix, symbols, log, init_printing, pprint, simplify, expand

matrix = lambda x: Matrix(x)
cvec = lambda x: Matrix(x)
rvec = lambda x: Matrix([x])

init_printing()

import sys


def ld_norm(M):
	diag_rsum = lambda m: Matrix([[m[0, 0] + m[0, 1], 0 ], [0, m[1, 0] + m[1, 1]]  ])
	d1 = diag_rsum(M).det()
	d2 = diag_rsum(M.T).det()
	return expand(d1 * d2)**(0.5)



def explogdet(M):
	diag_rsum = lambda m: Matrix([[m[0, 0] + m[0, 1], 0 ], [0, m[1, 0] + m[1, 1]]  ])
	detF = M.det()
	d1 = diag_rsum(M).det()
	d2 = diag_rsum(M.T).det()
	return expand(detF * detF) / expand(d1 * d2)
	


def freq(r, p):
	o = Matrix([
			[r[0] * p[0, 0], r[0] * p[0, 1]],
			[r[1] * p[1, 0], r[1] * p[1, 1]]])  
	#pp((r, p, o))
	return o

def pp(*x):
	print('=' * 100)
	pprint(*x)
	#print('*' * 100)


def markov_matrix2(p):
	p00, p11 = symbols('{0}00 {0}11'.format(p))
	return Matrix([[p00, 1-p00 ], [1-p11, p11]])


def markov_matrix2_1(p):
	p00, p11 = symbols('{0}00 {0}11'.format(p))
	return Matrix([[p00, 1-p00 ], [1-p00, p00]])
	


r0 = symbols('r0')
root = rvec([r0, 1-r0]) 
A = markov_matrix2('a')
B = markov_matrix2('b')

def main():

	#clear = lambda x: expand(x)
	path2 = explogdet(freq(root, A * B))
	path_a = explogdet(freq(root, A))
	path_b = explogdet(freq(root * A,  B))

	d = expand(path2 / (path_a * path_b))


	dhalf = d.subs(r0, 0.5)

	print('d', d) # simplify(path2))
	print('dhalf', dhalf  ) 




def main2():
	A = markov_matrix2_1('a')
	B = markov_matrix2_1('b')
	r_ab = freq(root, A*B)
	r_a = freq(root, A) 
	r_a_ra_b = freq(root*A, B)
	
	d = (r_ab.det()/ld_norm(r_ab )) / ((r_a.det() / ld_norm(r_a)) * (r_a_ra_b.det() / ld_norm(r_a_ra_b)))
	
	pp(r_ab)
	pp(r_a)
	pp(r_a_ra_b)
	x = r_ab[0, 0]
	y = (r_a*r_a_ra_b)[0, 0]
	print(simplify(x.subs(r0, 0.5)), simplify(y.subs(r0, 0.5)))
	pp(simplify(d.subs(r0, 0.5)))
	return 

	print(simplify(expand(d.subs(r0, 0.5))))


if __name__ == '__main__':
	main2()













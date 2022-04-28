from sympy import *

matrix = lambda x: Matrix(x)
cvec = lambda x: Matrix(x)
rvec = lambda x: Matrix([x])

init_printing()


def logdet(M):
	diag_rsum = lambda m: Matrix([[m[0, 0] + m[0, 1], 0 ], [0, m[1, 0] + m[1, 1]]  ])




def pp(*x):
	pprint(*x)


def markov_matrix2(p):
	p00, p11 = symbols('{0}00 {0}11'.format(p))
	return Matrix([[p00, 1-p00 ], [1-p11, p11]])

r0, r1 = symbols('r0 r1')

root = rvec([r1, 1-r1]) 
root_u = rvec([0.5, 0.5])

m = markov_matrix2('p') 

pp(m)


pp(rvec([1, 0]) * m )

pp(rvec([0, 1]) * m )



root_m = root * m

pp(simplify(root_m[0] + root_m[1]) )


pp(root_u * m)




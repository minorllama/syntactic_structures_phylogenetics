from sympy import *
init_printing(use_unicode=False)

matrix = lambda x: Matrix(x)
cvec = lambda x: Matrix(x)
rvec = lambda x: Matrix([x])

(p0, p1) = symbols('p0 p1')
(a00, a01, a11, a10) = symbols('a00 a01 a11 a10')
(b00, b01, b11, b10) = symbols('b00 b01 b11 b10')

ma = p1*a11 + p0*a01
mb = p1*b11 + p0*b01

var = (p1*a11*b11 + p0*a01*b01)*(1-ma)*(1-mb)
var = var + (p1*a11*b10 + p0*a01*b00)*(1-ma)*(0-mb)
var = var + (p1*a10*b11 + p0*a00*b01)*(0-ma)*(1-mb)
var = var + (p1*a10*b10 + p0*a00*b00)*(0-ma)*(0-mb)

def constraints(x):
	x = x.subs(a00, 1-a01)
	x = x.subs(a10, 1-a11)
	x = x.subs(b00, 1-b01)
	x = x.subs(b10, 1-b11)
	x = x.subs(p0, 1-p1)
	return x

A = matrix([[a11, a01], [a10, a00]])
B = matrix([[b11, b01], [b10, b00]])
varM = matrix([[p1*(1-p1), p1*(p1 - 1)], [p1*(p1-1), p1*(1 - p1)]])
AvarMB = A*varM*B.T
e1 = constraints(AvarMB[1, 1] - var)
print(simplify(e1), e1)


Ez = cvec([p1, p0])
e1 = cvec([1, 0])
e0 = cvec([0, 1])
varM = simplify(p1*((e1 - Ez)*(e1 - Ez).T) +   p0*((e0 - Ez)*(e0 - Ez).T))
varM = varM.subs(p0, 1-p1)
AvarMB = A*varM*B.T
e2 = constraints(AvarMB[1, 1] - var)
print(simplify(e2), e2)

print(factor(simplify(constraints(expand(var)))))

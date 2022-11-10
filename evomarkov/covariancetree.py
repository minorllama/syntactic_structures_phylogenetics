from pyext import *
import numpy as np
import pandas as pd
import ltx


def covariance(vec):
	hashed = dict()
	for a in vec:
		hashed[a] = dict()
		for b in vec:
			hashed[a][b] = np.cov([vec[a], vec[b]])[0, 1]
	return hashed


def getmaxpair(m):
	mindex = None
	maxsofar = -1
	for a in m:
		for b in m[a]:
			if a != b:
				if m[a][b] > maxsofar or mindex is None:
					maxsofar = m[a][b]
					mindex = (a, b)
				elif m[a][b] == maxsofar:
					if not (mindex == (a, b) or mindex == (b, a)):
						print('__warn__', a, b, maxsofar, mindex)
	return mindex

def covariancetree(m):
	if len(m) == 1:
		return m
	else:
		(ma, mb) = getmaxpair(m)
		mnew = dict()	
		for e1 in m:
			for e2 in m[e1]:
				if not e1 in [ma, mb] and not e2 in [ma, mb]:
					if not e1 in mnew: mnew[e1] = dict()
					mnew[e1][e2] = m[e1][e2]
		mnew[(ma, mb)] = dict()
		for e in m:
			if not e in [ma, mb]:
				mnew[(ma, mb)][e] = min(m[ma][e], m[mb][e])
				if not e in mnew: mnew[e] = dict()
				mnew[e][(ma, mb)] = mnew[(ma, mb)][e]

		
		return covariancetree(mnew)




import curator2

def tree_actual(opts):
	cfg = Json.loadf('config.json')
	langs = cfg['langs']['romance']
	data = curator2.LangData(langs, ['sswl', 'longo'], 'rom')
	vec = data.vectorized()
	vec = {l: np.array(vec[l]) for l in vec}
	print(len(vec['latin']), vec['latin'])
	cov = covariance(vec)
	tree = covariancetree(cov)
	print(tree)
	print(ltx.table(cov))

def tree_ml(cfg):
	#data = Json.loadf('./maxlikelihood2/vectorized.rom.sim0.json')
	
	data = Json.loadf('./data/simanalysis/simulation.json')
	langs = data[0].keys()
	n = 1000
	sim = {e : [r[e] for r in data[0:n]]  for e in langs } 
	vec = {l: np.array(sim[l]) for l in sim}
	cov = covariance(vec)
	frame = pd.DataFrame(cov)
	print(frame)
	tree = covariancetree(cov)
	print(tree)



if __name__ == '__main__':
	cfg = Top.cfg()
	if cfg.has('-ml'):
		print('__mltree__')
		tree_ml(cfg)
	else:
		tree_actual(cfg)





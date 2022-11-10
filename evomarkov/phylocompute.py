from phyloinvariant import PhyloInvariant
from pyext import Json, Top
from curator2 import LangData
from treemaker import Tree

import numpy as np

np.set_printoptions(linewidth=160)

def vectorized(langs, use_db):
	data = LangData(langs, use_db, '')
	print('#allset', langs, len(data.allset))
	#print(langs, use_db, data.vec.keys(), data.langs, data.allset)
	return (data.vectorized(), data)


def invariants(dets):
	return {"l_sup":max([abs(e) for e in dets]), "l_1":sum([abs(e) for e in dets])}
	

def phylo_ancient(cfg):
	langs = cfg['langs'] 
	ancient = list(langs.keys())
	(hashed, data) = vectorized(ancient, cfg['db'])
	hashed = {langs[k] : hashed[k] for k in hashed}
	allresults = dict()

	for analysis in [cfg["warnow"] , cfg['bouck'], cfg["logdet"], cfg['logdet2'], cfg['rexova']]:
		tag = cfg["family"] + "/" + analysis["tag"]
		leaves = analysis["leaves"]
		data = PhyloInvariant.vectorized2bdist(hashed, leaves)
		dets = list()
		for bipart in analysis["bipartitions"]:
			[u, v] = bipart
			phylo = PhyloInvariant(leaves, data['bdist'])
			(m, rows, cols, nonzeros) = phylo.flattening_matrix(u, v) 
			(bipart_dets, bipart_minors) = phylo.all3x3minors(m, rows, cols, nonzeros)
			#print(analysis['tag'], bipart, {"l_sup":max([abs(e) for e in bipart_dets] + [-1]), "l_1":sum([0] + [abs(e) for e in bipart_dets])})
			#print(m)
			dets.extend(bipart_dets) 

		result = {'invariannt' : analysis["tag"], 'all_dets' : invariants(dets) }
		assert not tag in allresults
		print(result)
		allresults[tag] = result
	
	return allresults 

def phylo_romance(cfg):
	langs = cfg['langs'] 
	romance = list(langs.keys())
	(hashed, data) = vectorized(romance, cfg['db'])
	hashed = {langs[k] : hashed[k] for k in hashed}

	allresults = dict()
	for analysis in [cfg["historical"], cfg["logdet"]]:
		tag = cfg["family"] + "/" + analysis["tag"]
		leaves = analysis["leaves"]
		data = PhyloInvariant.vectorized2bdist(hashed, leaves)
		dets = list()
		for bipart in analysis["bipartitions"]:
			[u, v] = bipart
			phylo = PhyloInvariant(leaves, data['bdist'])
			(m, rows, cols, nonzeros) = phylo.flattening_matrix(u, v)
			(bipart_dets, bipart_minors) = phylo.all3x3minors(m, rows, cols, nonzeros)
			dets.extend(bipart_dets)

		result = {'invariannt' : analysis["tag"], 'all_dets' : invariants(dets) }	
		assert not tag in allresults
		print(result)
		allresults[tag] = result
	
	return allresults

def phylo_uralic(cfg):
	langs = cfg['langs'] 
	uralic = list(langs.keys())
	(hashed, data) = vectorized(uralic, cfg['db'])
	hashed = {langs[k] : hashed[k] for k in hashed}

	allresults = dict()
	for tree_id, analysis in [(k, cfg[k]) for k in cfg["analysis"]]:
		tag = cfg["family"] + "/" + tree_id
		tree = Tree(analysis['tree']) 
		leaves = tree.leaves()
		data = PhyloInvariant.vectorized2bdist(hashed, leaves)
		dets = list()
		biparts = tree.nontrivial_biparts()
		for bipart in biparts:
			[u, v] = bipart
			phylo = PhyloInvariant(leaves, data['bdist'])
			(m, rows, cols, nonzeros) = phylo.flattening_matrix(u, v)
			(bipart_dets, bipart_minors) = phylo.all3x3minors(m, rows, cols, nonzeros)
			dets.extend(bipart_dets)

		result = {'invariannt' : tag, 'all_dets' : invariants(dets) }	
		assert not tag in allresults
		print(result)
		allresults[tag] = result
	
	return allresults



if __name__ == '__main__':
	top = Top.cfg()
	cfg = Json.loadf(top.or_else('-cfg', "./phyloconfig.json"))
	if not top.has('-fromtables'):
		r = dict()
		r['ancient'] = phylo_ancient(cfg['ancient'])
		r['romance'] = phylo_romance(cfg['romance'])
		r['uralic'] = phylo_uralic(cfg['uralic'])
		Json.pp(r)
		print(Json.dumpf('./data/phyloinvariants.json', r))
	else:
		import phylocompute_tsv
		r = dict()
		phylocompute_tsv.F1minors()
		r['ancient'] = phylocompute_tsv.phylo_tsv(cfg,'ancient', ["warnow", "bouck", "rexova"])
		r['germanic6'] = phylocompute_tsv.phylo_tsv(cfg,'germanic6', ["historical"])

		Json.pp(r)




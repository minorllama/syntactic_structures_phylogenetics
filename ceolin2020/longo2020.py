from pyext import *
import pandas as pd
import itertools as it
from logdet import LogDet
import treemaker
from collections import Counter
from ltx import latex_tree




class Longo2020:
	def __init__(self):
		self.data = pd.read_csv('./Data_Sheet_1_Formal_Syntax_and_Deep_History.csv', sep = ',', encoding='Latin1')
		self.hashed = self.data.to_dict()
		self.langs  = [k for k in self.hashed if not (k in ['Label', 'Label.2', 'Label.1', 'Parameter', 'Implication(s)'] or k.startswith('Unnamed'))]
		
		def rows(d):
			r = [e for e in list(range(95))] 
			for k in self.langs:
				assert len(d[k]) == 95
				assert sorted(list(d[k].keys())) == r, [d[k], r]
				assert d[k][94] == k or k[0:5] in ['Unnam', 'Label', 'Param', 'Impli'], [k, d[k][94]]
			return r[0:-1]
		
		self.paramfullindex = [k for k in rows(self.hashed)]
	
	def vec(self):
		def noentailment(index):
			newindex = list()
			for i in index:
				ok = [(e, i, str(self.hashed[e][i]).encode('utf-8') ) for e in self.langs if not str(self.hashed[e][i]) in '+-']
				print(str(ok))
				if len(ok) == 0 : #len(self.hashed):
					newindex.append(i)
			return newindex

		index = self.paramfullindex
		nounset = noentailment(index)
		data = dict()
		for k in self.langs:
			data[k] = [self.hashed[k][i] for i in index]
		return data

	def pairvec(self, l1, l2):
		av, bv = list(), list()
		code = {'+' : 1, '-' : 0 }
		for i in self.paramfullindex:
			if str(self.hashed[l1][i]) in '+-' and str(self.hashed[l2][i]) in '+-':
				a = self.hashed[l1][i]
				b = self.hashed[l2][i]
				av.append(code[a]) 
				bv.append(code[b])
			else:
				pass
		diff = [i for i in range(len(av)) if av[i] != bv[i]]
		return (av, bv, diff)


class LongoTable2020:
	def __init__(self):
		lines = [e.split() for e in Cmn.entries('./FormalSyntax/table.txt')]
		def tryint(y):
			assert y in '01?', y
			if y == '?': return y
			else: return int(y)
				
		hashed = dict()
		for e in lines:
			hashed[e[0]] = [tryint(x) for x in e[1:]]
		self.hashed = hashed
		self.langs = self.hashed.keys()
		self.familyindex = dict()
		self.th = 0.0
	def familyparamset(self, family):
		index = list(range(len(self.hashed[family[0]])))
		if not family in self.familyindex:
			self.familyindex[family] = [i for i in index if len([l for l in family if str(self.hashed[l][i]) in '+-01']) >=  self.th * len(family) ]
		return self.familyindex[family]

	def pairvec(self, a, b, family=None):
		u = self.hashed[a]
		v = self.hashed[b]
		index = list(range(len(u)))  if not family else self.familyparamset(family)
		#print(family, len(index), index)
		d1 = list()
		d2 = list()
		for i in index:
			if u[i] in [0, 1] and v[i] in [0, 1]:
				d1.append(u[i])
				d2.append(v[i])
		diff = [j for j in range(len(d1)) if d1[j] != d2[j]]
		return (d1, d2, diff)

def modified_jaccard(a, b):
	p, m = 1, 0
	assert len(a) == len(b)
	hashed = Counter([e for e in zip(a, b)])
	d = float(hashed[(p, m)] + hashed[(m, p)])/(hashed[(p, m)] + hashed[(m, p)] + hashed[(p, p)])
	return d




def main(family, metric=None, root=None):
	#longo = Longo2020()
	longo = LongoTable2020()
	logdet = LogDet([0, 1])
	d = dict()

	degenerate = ['Siciliano_Ragusa', 'Barese', 'Reggio_Emilia', 'Greek_Salento', 'Greek_Cypriot', 'Serbo-Croatian', 'Irish', 'Even_1', 'Even_2', 'Kazakh', 'Kirghiz', 'Archi']
	if family == 'all':
		langs = list(longo.langs)
		family = None
	elif family:
		langs = family
	else:
		langs = [l for l in longo.langs if not l in degenerate]

	for l1 in langs:
		d[l1] = dict()
		for l2 in langs:
			if l1 == l2:
				d[l1][l2] = 0.0
			elif l1 in d.get(l2, {}):
				d[l1][l2] = d[l2][l1]
			else:
				(av, bv, diff) = longo.pairvec(l1, l2, family=family)
				if not diff:
					print('bad', l1, l2, len(av))
					d[l1][l2] = 0
				else:
					if not metric:
						d[l1][l2] = logdet.evaluate(av, bv)		
					else:
						d[l1][l2] = metric(av, bv)

	treemaker.ascii_plot_width = 160
	#tree = treemaker.biopy_nj_ascii(d, langs, labels=None)
	(d2, tree) = treemaker.biopy_nj(d, langs, labels=None)
	if root:
		print("rooting", root)
		tree.root_with_outgroup(root)
		tree.ladderize(reverse=True)
	bptree = tree

	#tree = treemaker.skbio_nj_ascii(d, langs, labels=None)
	tree = treemaker.biopy_tree_draw(tree)
	tree_latex = latex_tree(tree)
	
	print(tree)
	print(langs)
	for k in longo.familyindex:
		print(k, len(longo.familyindex[k]), '__index__')
	(dist, t) = treemaker.biopy_nj(d, langs, labels=None)
	t = treemaker.skbio_nj_tree(d, langs, labels=None)
	return bptree, tree, dist, treemaker.skbio_to_newick(t), treemaker.skbio_nj_ascii(d, langs, labels=None), tree_latex


def analysis1():
	romance = tuple(list(sorted(['Siciliano_Mussomeli', 'Calabrese_Southern', 'Salentino', 'Calabrese_Northern', 'Campano', 'Teramano', 'Casalasco', 'Parma', 'Italian', 'Spanish', 'French', 'Portuguese', 'Romanian', 'Greek_Calabria_1', 'Greek_Calabria_2', 'Greek'])))

	germanic = tuple(list(sorted(['English', 'Dutch', 'Afrikaans', 'German', 'Danish', 'Icelandic', 'Faroese', 'Norwegian',  'Welsh'] )))

	#main(romance)
	#main(germanic)
	t1, d, t, sk = main(None)

	print(sk)

	nwk_tree = treemaker.biopy_to_newick(t)
	tupled = str(treemaker.biopy_nwk_to_tuple(nwk_tree)).replace("Inner", '').replace('"', '').replace(",",  ' ')

	print(nwk_tree)
	print(tupled)

if __name__ == "__main__":
	tree, dist, t, sk = main('all')
	import plotter3

	plotter3.heatmap(dist)
	print(plotter3.p.save())



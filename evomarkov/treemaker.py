from Bio.Phylo.TreeConstruction import DistanceTreeConstructor
from Bio.Phylo.TreeConstruction import DistanceMatrix
import Bio.Phylo
import io
import re
import numpy as np
from pyext import Cmn, Json

ascii_plot_width = 80
round_for_symmetry_digits = 8

def biopy_nj(data, taxa, labels=None):
	if not labels: labels = dict(zip(taxa, taxa))
	tmatrix = list()
	for n, l in enumerate(taxa):
		dist = [data[l][taxa[i]]  for i in range(n + 1)]
		tmatrix.append(dist)
	constructor = DistanceTreeConstructor()
	d = DistanceMatrix(names=[labels[e] for e in taxa], matrix=tmatrix)
	return (d, constructor.nj(d))


def biopy_nj_ascii(data, taxa, labels=None):
	(d, tree) = biopy_nj(data, taxa, labels)
	out = io.StringIO()
	Bio.Phylo.draw_ascii(tree, out, column_width=ascii_plot_width)
	out.flush()
	return out.getvalue()



def biopy_nj_draw(data, taxa, labels=None, clean_inner=True, axes=None):
	(d, tree) = biopy_nj(data, taxa, labels)
	seen = set()
	for e in tree.get_nonterminals():
		if clean_inner:
			e.name = e.name.replace('Inner', '')
			assert not e.name in seen
			seen.add(e.name)
	Bio.Phylo.draw(tree, show_confidence=False, axes=axes) 
	return tree

def biopy_to_newick(t):
	out = io.StringIO()
	Bio.Phylo.NewickIO.write([t], out)
	out.flush()
	return out.getvalue()

def biopy_nwk_to_tuple(t):
	dists = re.compile(":[0-9\.-]+")
	misc = re.compile("[0-9;]+")
	t2 = dists.sub('', t)
	t2 = misc.sub('', t2)
	labels = re.compile("[^,\(\)]+")
	all_labels = labels.findall(t2)
	for e in all_labels:
		t2 = t2.replace(e, '"{0}"'.format(e))
	return t2.replace("(", "[").replace(")", "]")
	
	

from skbio import DistanceMatrix as SKBDistanceMatrix
from skbio.tree import nj
from skbio.tree._tree import TreeNode as SKBioTreeNode
from skbio import read as skbio_read
from skbio.tree import TreeNode as SKBioTreeNode2



def skbio_nj_tree(data, taxa, labels=None):
	if not labels: labels = dict(zip(taxa, taxa))
	dist = [[np.around(data[a][b], round_for_symmetry_digits) for b in taxa] for a in taxa]
	dm = SKBDistanceMatrix(dist, [labels[e] for e in taxa])
	return nj(dm)

def skbio_nj_ascii(data, taxa, labels=None):
	#if not labels: labels = dict(zip(taxa, taxa))
	#dist = [[np.around(data[a][b], round_for_symmetry_digits) for b in taxa] for a in taxa]
	#dm = SKBDistanceMatrix(dist, [labels[e] for e in taxa])
	return skbio_nj_tree(data, taxa, labels).ascii_art()

def skbio_to_newick(t):
	out = io.StringIO()
	t.write(out, format='newick')
	out.flush()
	return out.getvalue()








class Tree:
	def __init__(self, t):
		self.tree = t
		self.is_internal = lambda x: isinstance(x, tuple) or isinstance(x, list)
	def leaves(self, tree=None):
		if tree == None: tree = self.tree
		def __leaves(tree, sofar):
			if self.is_internal(tree):
				for e in tree:
					__leaves(e, sofar)
			else:
				sofar.append(tree)
			return sofar
		return __leaves(tree, [])
	def biparts(self):
		tree = self.tree
		def bipart_subtree(tree, biparts, ancestral_tree_leaves):
			if self.is_internal(tree):
				assert len(tree) == 2
				leaves = [self.leaves(tree[0]), self.leaves(tree[1])]
				if ancestral_tree_leaves:
					biparts.append((leaves[0] + ancestral_tree_leaves, leaves[1]))
					biparts.append((leaves[0], leaves[1]  + ancestral_tree_leaves))
				else:
					biparts.append((leaves[0], leaves[1]))
				if self.is_internal(tree[0]):
					bipart_subtree(tree[0], biparts, ancestral_tree_leaves + leaves[1])
				if self.is_internal(tree[1]):
					bipart_subtree(tree[1], biparts, ancestral_tree_leaves + leaves[0])
			else:
				biparts.append((self.leaves(tree), ancestral_tree_leaves))
		bipartition_list = list()
		bipart_subtree(tree, bipartition_list, [])
		return bipartition_list
	def nontrivial_biparts(self):
		biparts = self.biparts()
		return [e for e in biparts if all(len(x) > 1 for x in biparts)]
	
def from_newick(tree):
	str_treedata = str(tree)
	return Bio.Phylo.read(io.StringIO(str_treedata), "newick")

def draw_ascii(tree):
	out = io.StringIO()
	Bio.Phylo.draw_ascii(tree, out, column_width=ascii_plot_width)
	out.flush()
	return out.getvalue()

def dump_phyfile(fname, data):
	# http://rosalind.info/glossary/phylip-format/
	n = Cmn.uniq([len(e) for e in data.values()])
	
	lines = []
	seen = dict()
	for k in sorted(list(data.keys())):
		seq = ''.join([str(int(e)) for e in data[k]])
		assert len(seq) == n
		z = k.replace(' ', '_')
		if not seq in seen:
			lines.append('{0}     {1}\n'.format(z, seq))
			seen[seq] = [z]
		else:
			seen[seq].append(z)
	header = '{0} {1}\n'.format(len(seen), n)
	lines = [header] + lines
	print(Json.dumpf(fname + '.dup.json', seen))
	return Cmn.dumpf(fname, ''.join(lines) + '\n')



def newick(tree):
	if isinstance(tree, SKBioTreeNode):
		return skbio_to_newick(tree)
	else:
		return  biopy_to_newick(tree)


def str_tree(tree):
	if isinstance(tree, SKBioTreeNode):
		return tree.ascii_art()
	else:
		out = io.StringIO()
		Bio.Phylo.draw_ascii(tree, out, column_width=ascii_plot_width)
		out.flush()
		return out.getvalue()

def ascii_art(tree):
	return str_tree(tree)


def ascii_tree(data, taxa, labels=None, skbio=True):
	if skbio:
		return skbio_nj_ascii(data, taxa, labels)
	else:
		return biopy_nj_ascii(data, taxa, labels)

def raw_tree(data, taxa, labels=None, skbio=True):
	if skbio:
		tree = skbio_nj_tree(data, taxa, labels)
		return (tree, tree.ascii_art())
	else:
		(d, tree) = biopy_nj(data, taxa, labels)
		return (tree, draw_ascii(tree))

def str_newick(s,skbio=False):
	if skbio:
		f = io.StringIO(s)
		return skbio_read(f, format="newick", into=SKBioTreeNode2)
	else:
		trees = Bio.Phylo.parse(io.StringIO(s), 'newick')
		return Cmn.uniq(list(trees))

def trees_equal(a, b, skbio=False):
	assert not skio
	clades = lambda a:{tuple(sorted([l.name for l in e.get_terminals()])) for e in a.get_nonterminals()}
	al = clades(a)
	bl = clades(b)
	return (al, bl, al == bl)

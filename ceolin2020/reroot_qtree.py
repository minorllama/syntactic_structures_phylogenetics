from io import StringIO
import treemaker as tm
import ltx
import re
from Bio import Phylo




def qtree2newick(t):
	t_in = t
	p3 = re.compile("\s+")
	p2 = re.compile("\s+\]")
	p = re.compile("\[\s+")
	t = p.sub("[", p2.sub("]", t))
	t = p3.sub(", ", t)
	t = t.replace("[", "(")
	t = t.replace("]", ")")
	print(t, t_in)
	return t

def reroot(t, root):
	t = qtree2newick(t)
	tree = Phylo.read(StringIO(t), "newick")
	tree.root_with_outgroup(root)
	t = tm.biopy_to_newick(tree)
	out = ltx.strqtree(t, '')
	p = re.compile("Inner[0-9]+")
	out = p.sub("", out)
	return out


rs = [
	("[  [  [  [  [  [  [  [  [  [ Fin Est ]  Udm2 ]  Mar2 ]   [  [ Kha2 Kha1 ]  Hun ]  ]  Udm1 ]  Mar1 ]  Bur ]   [ Yak Tur ]  ]  Uzb ]  Eve ]", ["Bur"])
]

for t, r in rs:
	print(reroot(t, r))


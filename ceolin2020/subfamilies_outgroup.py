from pyext import *
import longo2020
import treemaker
import ltx
import sys
import langcfg
import re

def treestrings(family, root, metric, tag):
	bptree, tree, dist, t, skbio, tree_latex = longo2020.main(family, metric, root=root)
	out = treemaker.biopy_to_newick(bptree)
	out = ltx.strqtree(out, family)
	p = re.compile("Inner[0-9]+")	
	out = p.sub("", out)	
	qtree = ltx.strqtree(t, family) 
	ascii_tree = "\subsection{" + tag + "}\n" + tree_latex
	return ("{1} $${0}$$".format(out.strip(), tag), ascii_tree, out)

def main():
	strtrees = list()
	qtrees = list()
	select = sys.argv[1] if len(sys.argv) > 1 else None
	langs = langcfg.langs() 
	outgroup = langcfg.outgroup()
	for name, family in sorted(langs.items()): 
		if not name == select and not select is None : continue
		else:
			print(family)

		root=outgroup[name]
		tag = name + ",outgroup:" + outgroup[name] + ":logdet"
		(qtree, atree, out) = treestrings(family, root, None, tag)
		qtrees.append(atree)
		strtrees.append(qtree)
		tag = name + ",outgroup:" + outgroup[name] + ":modified jaccard"
		(qtree, atree, out) = treestrings(family, root, longo2020.modified_jaccard, tag)
		qtrees.append(atree)
		strtrees.append(qtree) 
		strtrees.append("\n\n")	
	Top.dumpf("./outgrouped/trees_outgroup.tex", qtrees)
	Top.dumpf("./outgrouped/strtrees_outgroup.tex", strtrees)

def main_jaccard():
	for family in [germanic, romance, ie, ia, slavic, ua]:
			longo2020.main(family, longo2020.modified_jaccard)

if __name__ == '__main__':
	main()

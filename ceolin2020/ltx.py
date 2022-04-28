import re
from pyext import Json
import pandas as pd


codes = Json.loadf("dataconfig.json")["codes"]

def table(hashed, transpose=False):
	if isinstance(hashed, dict):
		frame = pd.DataFrame(hashed)
	else:
		frame = hashed
	
	if transpose:
		frame = frame.transpose()
	
	return frame.to_latex()

def newick_qtree(t):
	t = t.replace('(',  ' [ ')
	t = t.replace(')', ' ] ' )
	dists = re.compile(":[0-9\.-]+")
	misc = re.compile("^_[0-9;]+")
	t2 = dists.sub('', t)
	t2 = misc.sub('', t2).replace(',', ' ')
	trunc_langs = sorted(list(codes.keys()), key = lambda x: len(x), reverse=True)
	for l in trunc_langs:
		t2 = t2.replace(l, l[0:3])
	return t2.replace(";", "").strip()

def clean_ascii_tree(t):
	right_trailing_underscore = dists = re.compile("_+$")
	return '\n'.join([right_trailing_underscore.sub('', e) for e in t.splitlines()])


def latex_tree(t, label="..."):
	return """\\begin{figure}[H]
\\begin{center}
{
\\fontfamily{courier}\selectfont
\\begin{verbatim}\n\n""" + t + """\n\n\\end{verbatim}
}
\\label{"""  + label + """}
\\end{center}
\\end{figure}"""






def strqtree(tree, langs):
	t = newick_qtree(tree)
	t2 = "\Tree" + t + "\n\n"
	if not langs: return "\Tree" + t + "\n\n" 
	else:
		tags = set()
		langs = sorted(langs, key = lambda x: len(x), reverse = True)
		for e in langs:
			tag = e[0:3]
			if e.endswith("_1") or e.endswith("_2"):
				tag = tag + e.split("_")[-1]
			elif e.endswith("_Northern"): 
				tag = tag + ".N"
			elif e.endswith("_Southern"):
				tag = tag + ".S"
			assert not tag in tags, [tag, tags, langs]
			tags.add(tag)
			t = t.replace(e, tag)
		return "\Tree" + t + "\n\n"

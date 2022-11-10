import re
from pyext import Json
import pandas as pd


codes = Json.loadf("./config.json")["codes"]

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
	misc = re.compile("[0-9;]+")
	t2 = dists.sub('', t)
	t2 = misc.sub('', t2).replace(',', ' ')
	trunc_langs = sorted(list(codes.keys()), key = lambda x: len(x), reverse=True)
	for l in trunc_langs:
		t2 = t2.replace(l, l[0:3])
	return t2

def clean_ascii_tree(t):
	right_trailing_underscore = dists = re.compile("_+$")
	return '\n'.join([right_trailing_underscore.sub('', e) for e in t.splitlines()])

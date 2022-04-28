from pyext import *
import sys
sys.path.append("..")
import ltx 


from curator2 import LangData
LangData.dataconfig = "./dataconfig.json"

import longo2020
import treemaker
from logdet import LogDet


import pandas as pd

def dist(vec, metric):
	data = dict()
	for l in vec:
		if not l in data: data[l] = dict()
		for l2 in vec:
			if not l2 in data[l]: data[l][l2] = dict()
			if l != l2:
				if l in data.get(l2, {}):
					data[l][l2] = data[l2][l] 
				else:
					data[l][l2] = metric(vec[l], vec[l2])
			else:
				data[l][l2] = 0
	return data
def main():
	logdet = LogDet([0, 1])
	cfg = Json.loadf(LangData.dataconfig)
	langs = cfg["langs"]["romance"]
	analysis = ["sswl", "longo"]
	family = "romance"
	data = LangData(langs, analysis, family)	
	paramlist = data.allset
	vec = data.vectorized(paramlist)
	metrics = [("logdet", logdet.evaluate), ("mod_jaccard", longo2020.modified_jaccard)]
	for k, m in metrics:
		d = dist(vec, m)
		frame = pd.DataFrame(d)
		treemaker.ascii_plot_width = 160
		#tree = treemaker.biopy_nj_ascii(d, langs, labels=None)
		#print(tree)
		t = treemaker.skbio_nj_ascii(d, langs, labels=None)
		print(k)
		print(t)
		print(ltx.table(frame))
		

if __name__ == '__main__':
	main()


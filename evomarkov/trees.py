from pyext import Json, Cmn, Top
from curator2 import LangData
import random

import logdet
import treemaker

import pandas as pd

import ltx


__meta__ = Json.loadf('./config.json')
__cfg__ = Top.cfg()
verbose = __cfg__.has('-v')
latex = __cfg__.has('-latex')

def log_v(m):
	if __cfg__.has('-v'):
		print(m)


def distortion(langs, family):
	all_analysis = {'sswl': ['sswl'], 'longo': ['longo'], 'sswl+longo': ['sswl', 'longo']}
	vec, dist, states, data = dict(), dict(), dict(), dict()
	for k, analysis in all_analysis.items():
		data[k] = LangData(langs, analysis, family)
		vec[k] = data[k].vectorized(params=data[k].allset)
		dist[k], states[k] = logdet.dmatrix(vec[k])
		print(k, len(data[k].allset))
		print(pd.DataFrame(dist[k]))

def tree_with_params(data, langs, analysis_type, family, skbio, paramlist=None):
	if not paramlist: paramlist = data.allset
	vectorized = data.vectorized(paramlist)
	try:	
		dist, states = logdet.dmatrix(vectorized)
		assert states == [0.0, 1.0]
		(t, t_art) = treemaker.raw_tree(dist, langs, skbio=skbio)
		return (t, t_art, paramlist, dist)
	except Exception as e:
		print('#except', e)
		return (None, None, paramlist, None)

def tree(langs, analysis_type, family, skbio):
	data = LangData(langs, analysis_type, family)
	if verbose:
		print('# allset', langs, len(data.allset))
	t, t_art, paramlist, dist = tree_with_params(data, langs, analysis_type, family, skbio, paramlist= data.allset)
	return (t_art, len(data.allset), treemaker.newick(t), dist)


def tree_explore(langs, analysis_type, family, skbio):
	data = LangData(langs, analysis_type, family)
	if __cfg__.has('-rexova-params'):
		rexova_params1 = [0, 1, 2, 4, 5, 6, 7, 8, 12, 15, 17, 18, 19] 
		rexova_params0 = [20, 21] + [13, 3]
		index = rexova_params1 + rexova_params0
		tag = family + "_rexova"
	else:
		tag = family
		index = list(range(len(data.allset)))
	log = list()
	logfile = "./generated_feb2021/" + tag
	Cmn.mkdir(logfile)
	logfile = logfile + "/" + tag + "." + Cmn.now() + ".trials.txt"

	for z in range(int(__cfg__.or_else('-trials', 1))):
		for k_frac in __meta__['param_subsampling']:
			k = int(k_frac * len(data.allset))
			opts = {'range': sorted(random.sample(index, k=k)) }
			paramlist = [data.allset[e] for e in opts['range']]
			(t, t_art, params, dist) = tree_with_params(data, langs, analysis_type, family, skbio, paramlist)
			if not t:
				print('# tree', k, '__fail__')
				log.append('# tree  {0} __faile__'.format(k))
			else:
				nt = ltx.newick_qtree(treemaker.newick(t)).replace("Inner", "")
				print('# tree', k, nt)
				print('# ', z, k , opts, len(opts['range']))
				print(t_art)
				msg = '# tree {0}\t{1}\tz={2}:k={3} actual={4} allset={5} %={6} \n#{7}\n\n'.format(nt.strip(),"kfrac:{0}".format(k_frac), z, k, len(opts['range']), len(data.allset),  float(len(opts['range']))/len(data.allset),  opts['range'])
				log.append(msg + "\n" + t_art+"\n\n") 

	print(Cmn.dumpf(logfile, log))

	if __cfg__.has('-ancient'): 

		parameters_reconstruct = [0, 1, 2, 4, 5, 6, 7, 8, 12, 15, 17, 18, 19]
		
		paramlist = [data.allset[e] for e in parameters_reconstruct]
		(t, t_art, params, dist) = tree_with_params(data, langs, analysis_type, family, skbio, paramlist)
		print(ltx.table(dist) if latex else pd.DataFrame(dist))
		print(parameters_reconstruct, len(parameters_reconstruct))
		print(t_art)
		nt = ltx.newick_qtree(treemaker.newick(t))
		print(nt)
		log_v(params)

		parameters_reconstruct.extend([20, 21] + [13, 3]) # 9 10 14 16 11 bad maybe 11
		paramlist = [data.allset[e] for e in parameters_reconstruct]
		(t, t_art, params, dist) = tree_with_params(data, langs, analysis_type, family, skbio, paramlist)
		print(ltx.table(dist) if latex else pd.DataFrame(dist))
		print(parameters_reconstruct, len(parameters_reconstruct))
		print(t_art)
		print(ltx.newick_qtree(treemaker.newick(t)))
		log_v(params)







def main(cfg):
	opts = Json.loadf("./config.json")
	if cfg.has('-uralic'):
		selected = ['uralic_small', 'altaic-uralic']
	elif cfg.has('-uralic_small'):
		selected = ['uralic_small']
	elif cfg.has('-germanic'):
		selected = ["germanic"]
	elif cfg.has('-slavic'):
		selected = ['slavic']
	elif cfg.has('-slavic-small'):
		selected = ['slavic_no_slovenian']
	elif cfg.has('-ancient'):
		selected = ['ancient']
	elif cfg.has('-rom'):
		selected = ['romance']
	else:
		assert "__no_family__"

	if cfg.has('-w'): treemaker.ascii_plot_width = int(cfg['-w'])
	skbio = cfg.has('-skbio')	
	if cfg.has('-v'): verbose = True


	if cfg.has('-distortion'):
		distortion(opts["langs"]["slavic"], "slavic")
		return
	
	
	opts = Json.loadf("./config.json")
	for analysis in opts["analysis"]:
		family = analysis["family"]
		langs = opts["langs"][family]
		analysis_type = analysis["analysis_type"]
		print('skipping', family)
		
		if cfg.has('-alldb') and not set(['sswl', 'longo']) == set(analysis_type):
			print('skipping', family, analysis_type)
			continue

		if family in selected:
			if cfg.has('-explore'):
				tree_explore(langs, analysis_type, family,skbio)
			else:
				(ascii_tree, n_params, newick, dist) = tree(langs, analysis_type, family,skbio)
				print(family, n_params, analysis_type, ltx.newick_qtree(newick))
				print(ascii_tree)
				if __cfg__.has('-v'):
					print(print(ltx.table(dist) if latex else pd.DataFrame(dist)))
	
if __name__ == '__main__':
	main(__cfg__)





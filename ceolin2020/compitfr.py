import longo2020
from pyext import *
from subfamilies import tuplize, splitlangs
import pandas as pd
import ltx


def french_italian():
	hashed = dict()
	fr = "French"
	its = tuplize(splitlangs("Casalasco, Reggio_Emilia, Parma, Siciliano_Ragusa, Siciliano_Mussomeli, Salentino, Calabrese_Southern, Italian, Barese, Campano, Teramano, Calabrese_Northern"))
	for it1 in list(its) + ["French"]:
		if not it1 in hashed: hashed[it1] = dict()
		for it2 in its:
			if it1 != it2:
				longo = longo2020.LongoTable2020()
				(a, b, diff) = longo.pairvec(it1, it2, family=None)
				hashed[it1][it2] = int(len([i for i, x in enumerate(a) if not a[i] == b[i] ]))  	

	frame = pd.DataFrame(hashed).fillna(0)
	#frame.loc["Total"] = frame.sum()
	print(frame)
	print(ltx.table(frame))


french_italian()

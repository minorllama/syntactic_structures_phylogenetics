from pyext import *
import longo2020
import treemaker
import ltx

def nodegenerate(es):
	degenerate = ['Siciliano_Ragusa', 'Barese', 'Reggio_Emilia', 'Greek_Salento', 'Greek_Cypriot', 'Serbo-Croatian', 'Irish', 'Even_1', 'Even_2', 'Kazakh', 'Kirghiz', 'Archi']
	return [e for e in es if not e in degenerate]

tuplize = lambda x: tuple(nodegenerate(list(sorted(x))))
splitlangs = lambda x: [e.strip()  for e in x.split(",")]



germanic = tuplize(['English', 'Dutch', 'Afrikaans', 'German', 'Danish', 'Icelandic', 'Faroese', 'Norwegian',  'Welsh'])  

romance = tuplize(['Siciliano_Mussomeli', 'Calabrese_Southern', 'Salentino', 'Calabrese_Northern', 'Campano', 'Teramano', 'Casalasco', 'Parma', 'Italian', 'Spanish', 'French', 'Portuguese', 'Romanian', 'Greek_Calabria_1', 'Greek_Calabria_2', 'Greek'])

ie = tuplize(splitlangs("Irish, Welsh, Marathi, Hindi, Pashto, Greek, Greek_Cypriot, Greek_Calabria_1, Greek_Calabria_2,Greek_Salento, Bulgarian, Serbo-Croatian, Slovenian, Polish, Russian, Faroese, Norwegian, Danish,Icelandic, German, Dutch, English, Afrikaans, French, Casalasco, Reggio_Emilia, Parma, Spanish,Portuguese, Romanian, Siciliano_Ragusa, Siciliano_Mussomeli, Salentino, Calabrese_Southern, Italian, Barese, Campano, Teramano, Calabrese_Northern"))

slavic = tuplize(splitlangs("Bulgarian, Serbo-Croatian, Slovenian, Polish, Russian"))

ia = tuplize(splitlangs("Hindi, Marathi, Pashto, Tamil, Telugu"))

ua = tuplize(splitlangs("Kazakh, Kirghiz, Turkish, Yakut, Uzbek, Evenki, Even_1, Even_2, Buryat, Mari_1, Mari_2, Udmurt_1, Udmurt_2, Hungarian, Khanty_1, Khanty_2, Estonian, Finnish"))



def strqtree(tree, langs):
	t = ltx.newick_qtree(tree)
	t2 = "\Tree" + t + "\n\n"
	if langs:
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
def main():
	lines = list()
	qtrees = list()
	langs = {"germanic" : germanic, "romance" : romance, "indo-european": ie, "indo-aryan":ia, "slavic" : slavic,  "uralic-altaic": ua}
	for name, family in langs.items(): 
		if not name == "germanic": continue
		else:
			print(family)

		tree, dist, t, skbio, tree_latex = longo2020.main(family, root="Welsh")
		qtree = strqtree(t, family)
		qtree = tree_latex	
		qtrees.append("\subsection{" + name + ":logdet}")
		qtrees.append(qtree)
		#qtrees.append(tree_latex) 

		tree, dist, t, skbio, tree_latex = longo2020.main(family, longo2020.modified_jaccard, root="Welsh")
		qtree = strqtree(t, family)
		qtree = tree_latex
		qtrees.append("\subsection{" + name + ":modified jaccard}")
		qtrees.append(qtree)
		#qtrees.append(tree_latex)

	Top.dumpf("trees.tex", qtrees)
def main_jaccard():
	for family in [germanic, romance, ie, ia, slavic, ua]:
			longo2020.main(family, longo2020.modified_jaccard)

if __name__ == '__main__':
	main()

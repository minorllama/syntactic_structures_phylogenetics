from pyext import Json
import pandas as pd
import math

__verbose__ = False


class Curator:
	def isnan(self, x):
		try: return math.isnan(float(x))
		except: print(x)
		return False
	def no_float_keys(self, d):
		return d[[e for e in d.columns if not isinstance(e,  float)]]
	def clean_sswl_spreadsheet(self, hashed):
		for l in hashed:
			#print(l, hashed.keys())
			#x3.Json.pp(hashed)
			if l.lower().find('arabic') != -1:
				if self.verbose: print('#....', l,len( [e for e in hashed[l] if not self.isnan(hashed[l][e])]))
		for l in ['Maori', 'Papuan Malay', 'Tukang Besi']: # garbage in spreadsheet?
			hashed[l]['latlong'] = 0
		hashed2 = dict()
		for l in hashed:
			hashed2[l] = dict()
			for p in hashed[l]:
				x = hashed[l][p]
				if math.isnan(x): x = float("nan")
				elif x > 0: x = 1.0
				elif x < 0: x = -1.0
				else: assert x == 0
				hashed2[l][p] = x
		return hashed2
	def __init__(self):
		def parse(e):
			[a, b]  = e.split('(')
			a = a.strip()
			b = b.strip().strip(')')
			return (b, a)
		self.verbose = False
		self.translate = dict([parse(e) for e in '''Kadiweu (Ka), Kuikuro (Ku), Ragusa (RGS), Mussomeli (MuS), Aidone (AdS), Northern Calabrese (NCa), Southern Calabrese (SCa), Salentino (Sal), Campano (Cam), Italian (It), Spanish (Sp), French (Fr), Portuguese (Ptg), Romanian (Rm), Latin (Lat), Classical Greek (ClG), New Testament Greek (NTG), Salento Greek (SaG), Calabrian Greek A (CGA), Calabrian Greek B (CGB), Greek (Grk), Romeyka Pontic Greek (RPG), Cypriot Greek (CyG), Gothic (Got), Old English (OE), English (E), German (D), Danish (Da), Icelandic (Ice), Norwegian (Nor), Bulgarian (Blg), Serb-Croatian (SC), Slovenian (Slo), Polish (Po), Russian (Rus), Irish (Ir), Welsh (Wel), Marathi (Ma), Hindi (Hi), Farsi (Far), Pashto (Pas), Mandarin (Man), Cantonese (Can), Inuktitut (Inu), Japanese (Jap), Korean (Kor), Arabic (Ar), Hebrew (Heb), Hungarian (Hu), Khanty (Kh), Estonian (Est), Udmurt (Ud), Yukaghir (Yu), Even (Ev), Evenki (Ek), Yakut (Ya), Turkish (Tur), Buryat (Bur), Central Basque (cB), Western Basque (wB), Wolof (Wo)'''.split(',')])
		assert self.translate['SC'] == 'Serb-Croatian' and self.translate['Slo'] == 'Slovenian', self.translate
		self.translate2 = {
			'arabic':	'Arabic, Gulf'.lower(), #:  'arabic',
			'classical greek' :'Ancient Greek'.lower(), #: 'cig',	
			'greek (pontic)' : 'romeyka pontic greek',
			'northern calabrese' : 'calabrian (northern)',
			'ancient greek' : 'classical greek', #:'Ancient Greek'.lower(),
		}
		logs = (Json.dumpf("./parsed/translate.json", self.translate), Json.dumpf("./parsed/translate2.json", self.translate2))
		if __verbose__:print(log)

	def load_longo(self, f, to_replace):
		data = pd.read_csv(f)
		#hashed = data.to_dict()
		data2 = data.replace(to_replace)
		data3 = data2[data2.columns].astype(float) # cast types
		#print('longo.shape', data3.shape)
		return data3
	def load_sswl(self, f):
		data = pd.read_excel(f,  index_col=0).transpose()
		data2 = self.no_float_keys(data)
		hashed = self.clean_sswl_spreadsheet(data2.to_dict())
		data3 = pd.DataFrame(hashed)
		#print('sswl.shape', data3.shape)
		return data3


def load_sswl_longo(to_replace_longo, opts=None):
	if not opts: opts = dict()
	curate = Curator()
	#if use_ternary:
	#   to_replace = {'+' :  1, '-' : 0, '?' : float("nan"), '0' : 2}
	#else:
	#   to_replace = {'+' :  1, '-' : 0, '?' : float("nan"), '0' :  float("nan") }   #, '0' : float("nan"), 0:float("nan")}
	# check that data does not contain any floating point 0 but only has string 0s = "0"
	# >>> data = pd.read_csv("./raw/longobardi.csv")
	# >>> data2 = data.replace({0:1000})
	# >>> data3 = data.replace({'0':1000})
	# >>> data.equals(data2)
	# True
	# >>> data.equals(data3)
	# False
	
	longo_loaded = curate.load_longo("./raw/longobardi.csv", to_replace=to_replace_longo)
	longo = longo_loaded.transpose()
	longo2 = longo.to_dict()
	longo3 = {curate.translate.get(e, e).lower() : longo2[e] for e in longo2}
	#print(longo3['slovenian'])
	assert len(longo3) == len(longo2)
	print("#longo", longo_loaded.shape, Json.dumpf("./parsed/longobardi.json", longo3), Json.dumpf("./parsed/longobardi_raw.json", longo2))

	sswl_loaded = curate.load_sswl("./raw/sswl.xlsx")
	sswl = sswl_loaded.to_dict()
	sswl = {k.lower().replace(' ', '_')  : sswl[k] for k in sswl}
	sswl_log = Json.dumpf("./parsed/sswl.json", sswl)
	sswl["portuguese"] = sswl['european_portuguese']
	sswl["serb-croatian"] = sswl['serbian']
	print("#sswl", sswl_loaded.shape, Json.dumpf("./parsed/sswl_raw.json", sswl ), sswl_log)
	
	# edits
	#print(sswl['hittite'].keys())
	# fixes for updated parameters
	if 'fix_updated_params' in opts:
		print('# unrolling hittite/armenian update params')
		sswl['hittite']['11_Adposition Noun_Phrase'] = 0
		sswl['western_armenian']['Neg 01_Standard Negation is Particle that Precedes the Verb'] = 1.0
	
	return (sswl,  longo3)

def vectorized(langs, use_db, to_replace_longo, opts):
	(sswl, longo) = load_sswl_longo(to_replace_longo, opts)
	#print(longo['slovenian'], len(longo['slovenian']))
	#print(sswl.keys())
	hashed = dict()
	for l in langs:
		hashed[l] = dict()
		dbs = list()
		if 'sswl' in use_db: dbs.append(sswl)
		if 'longo' in use_db: dbs.append(longo)
		for db in dbs:
			if not l in db: print(["__missing_lang__", l, sorted(list(db.keys()))])
			for p in db[l]:
				assert not p in hashed[l]
				hashed[l][p] = db[l][p]
	return hashed


class LangData:
	dataconfig = './config.json'
	def __init__(self, langs, use_db, tag, opts=None):
		self.opts = opts if opts else dict()
		cfg = Json.loadf(LangData.dataconfig) #('config.json')
		if 'fix_updated_params' in cfg: 
			self.opts['fix_updated_params'] = True
			print('#opts', self.opts)
		self.tag = tag
		self.use_db = use_db
		for e in use_db: assert e in ['longo', 'sswl']
		self.to_replace =  {'+' :  1, '-' : 0, '?' : float("nan"), '0' :  float("nan")}
		self.vec = vectorized(langs, self.use_db, self.to_replace, self.opts)
		self.langs = langs
		paramlist = self.vec[langs[0]]
		self.allset = sorted([param for param in paramlist if all(not math.isnan(self.vec[l][param]) for l in langs)])
		self.paramlist = paramlist
	def vectorized(self, params=None):
		if not params: params = self.allset
		for l in self.langs:
			assert l in self.vec, [l, self.vec.keys()]
			for p in params:
				assert p in self.vec[l], [l, p, self.vec[l].keys()]
		return {l : [self.vec[l][p] for p in params] for l in self.langs}
	def param_vectorized(self):
		params = self.allset
		langs = sorted(self.langs)
		return {p: [self.vec[l][p] for l in langs] for p in params}




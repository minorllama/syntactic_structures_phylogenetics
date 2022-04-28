from . import utils
import sys

class Config:
	def __init__(self, args):
		keyargs = dict()
		def argtype(x):
			if x.strip()[0] != '-': return 'values'
			else:
				tokens = x.split(':')
				t = len(tokens)
				if t == 2:
					if tokens[0] in keyargs: raise Exception('malformed arguments '+ str(args) )
					else: keyargs[tokens[0]] = tokens[1]
				elif t == 1: return 'flags'
				else: raise Exception('malformed arguments '+ str(x))
		self.utils = utils.Utils()	
		parsed = self.utils.by_keyvalue(args, kf = lambda x: argtype(x), vf = lambda x: x)
		self.values, self.keys, self.flags = parsed.get('values', []), keyargs, parsed.get('flags', [])
		self.args = lambda : self.get_values()
		self.array = lambda : self.get_values()
	def __contains__(self, k):
		return k in self.keys or k in self.flags

	def __getitem__(self, k):
		if k in self.keys: return self.keys[k]
		elif k in self.flags: return True
		else:
			raise Exception('__MISSING__')

	def vals(self, k='-vals'):
		if k in self.keys:
			return self.utils.fentries(self.keys[k])
		else:
			return self.get_values()

	def get_values(self):
		return self.values

	def get(self, k, defaultvalue = None):
		if not defaultvalue: return self.keys[k]
		else: return self.keys.get(k, defaultvalue)

	def or_else(self, k, defaultValue):
		return self.keys.get(k, defaultValue) 

	def has(self, flag):
		return flag in self.flags or flag in self.keys.keys()

	def option(self, field):
		return self.keys[field] 

	def __str__(self):
		return '#config = -flags:{0} -keys:{1} values:{2}'.format(self.flags, self.keys, self.values)

	def cfgid(self, k='-tag'):
		if k in self.keys: return self.keys[k]
		return utils.timestamp() 

	@staticmethod
	def sys():
		return Config(sys.argv[1:])


def from_array(a):
	return Config(a)

def from_raw(a, k, f):
	cfg = Config([])
	cfg.keys = k
	cfg.values = a
	cfg.flags = f
	return cfg

def clargs():
	return Config.sys()

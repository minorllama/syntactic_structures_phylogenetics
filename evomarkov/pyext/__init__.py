from . import utils
from . import logger
from . import config
from . import cext
from .logging import Logging

def bashscript():
	return utils.Script()

def clargs():
	return config.clargs()


class TopCfgLog:
	def __init__(self, cfg):
		self.cfg = {k: cfg[k] for k in cfg}
		self.verbose = '-v' in cfg or '--verbose' in cfg or '-verbose' in cfg
		self.std = True
	def __call__(self, *m):
		if self.verbose and self.std:
			print(*m)		


class TopLevel:
	def __init__(self):
		self.msgtypes = {
                        'header'  : '\033[95m',
                        'blue'    : '\033[94m',
                        'green'   : '\033[92m',
                        'warn'    : '\033[93m',
                        'fail'    : '\033[91m',
                        'endc'    : '\033[0m',
                        'bold'    : '\033[1m',
        }        
		self.cext = cext
		self.log = utils.Logger() 
		self.json = utils.Json()
		self.cmn = utils.Utils()
		self.out = utils.OutputFiles()
		self.read = utils.LoadFiles()
		self.term = utils.Console()
		self.hold_on_warn = 0
	def cfg(self, array=None):
		if not array:
			return config.clargs()
		else:
			raise NotImplementedError("...")
	def color_str(self, m, c=None):
		if not c: c="green"
		return '{0}{1}{2}'.format(self.msgtypes.get(c, self.msgtypes["green"]), m, self.msgtypes['endc'])
	def warn(self, m="..."):
		m = self.color_str(m)
		if self.hold_on_warn > 0:
			import time
			self.sleep(self.hold_on_warn)
			return None
		else:
			entry = input(m)	
			return entry
	
	def find(self, pattern, loc=None,flags=None, relax=False):
		if not flags: flags = ['-name']
		if not loc: loc = "."
		cmd = ['find', loc] + flags + [pattern]
		found = self.cmn.shell(cmd)
		assert found['return'] == 0 or relax
		found["flist"] = [e for e in found["out"].splitlines()]
		return found

	def getlogger(self, cfg):
		opts = dict(list(cfg.keys.items()) + [(k, None) for k in cfg.flags])
		return TopCfgLog(opts)

Top = TopLevel()

Log = Top.log
Json = Top.json
Cmn = Top.cmn
Out = Top.out
Read = Top.read
Term = Top.term

json2 = Top.json
Json2 = Top.json
ext = Top.cmn
cmn = Top.cmn
Cmn2 = Top.cmn




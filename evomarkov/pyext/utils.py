import json
import os 
import sys
import time
import subprocess
from collections import defaultdict
import types
import pandas


def timestamp():
	current = time.ctime().split()
	return ('-'.join(current[1:3] + [current[-1], current[-2]])).replace(':', '.')







class Shell:
	def __init__(self):
		self.shell = ['#!/bin/bash'] 
	def cmd(self, c):
		self.shell.append('{0}\n\techo "return:$? {0} "\n\n'.format(c))
	def write(self, f):
		with open(f, 'w') as out:
			for e in self.shell:
				out.write(e)
				out.write('\n')
		return f


class NonUniqException(Exception):
	def __init__(self, msg,  at_val, collection, so_far):
		self.state = (at_val, so_far)
		self.collection = collection
		self.msg = msg

class Utils:
	def __init__(self):
		self.config = dict()
		self.log = lambda x: sys.stderr.write(u'{0}\n'.format(x))

	def mkdir(self, path):
		os.makedirs(path, exist_ok=True)
		return path

	def shell(self, cmd, verbose=False):
		try:
			shell_command = subprocess.Popen(cmd, shell=True , stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			[stdout, stderr] = shell_command.communicate()
			return dict(zip(['cmd', 'out', 'err', 'return', 'pid'], [cmd, stdout, stderr, shell_command.returncode, shell_command.pid]))
		except Exception as err:
			shell_command.terminate()
			return dict(zip(['cmd', 'out', 'err', 'return', 'pid'], [cmd, '', 'EXCEPTION:{0}'.format(str(err)), -1, -1]))
	def fread(self, f, gzip=False):
		if gzip:
			import gzip
			with gzip.open(f) as infile:
				return infile.read()
		else:
			with open(f) as infile:
				return infile.read()
	def fentries(self, fname, f=None):
		if f is None: f = lambda x: x.strip()
		with open(fname) as infile:
			return [f(e) for e in infile]
	def entries(self, f):
		return self.fentries(f)
	def flines(self, fname, f=None):
		with open(fname) as infile:
			if f:
				return list(map(f, infile.readlines()))
			else:
				return infile.readlines()
	def writel(self, f, entries, sep='\n'):
		with open(f, "w") as outfile:
			outfile.write(sep.join(entries))
		return f

	def dumpf(self, f, data, sep='\n'):
		if isinstance(data, str):
			with open(f, "w") as outfile:
				outfile.write(data)
			return f
		else:
			return self.writel(f, data,sep)
		
		
	def fexists(self, filename):
		if os.path.exists(filename): return True
		try:
			with open(filename) as test:
				return True
		except IOError: return False
	def exists(self, f):
		return self.fexists(f)
	
	def uniq(self, iterable):
		if len(iterable) == 1:
			return iterable[0]
		uniq = set()
		for e in iterable:
			uniq.add(e)
			if len(uniq) > 1:
				raise NonUniqException('#__non_uniq__', e, iterable, uniq)
		if len(uniq) != 1:
			raise NonUniqException('#__non_uniq__', None, iterable, uniq)
		return iterable[0]

	def demanduniq(self, es):
		return self.uniq(es)

	def safedict(self, tuples):
		hashed = dict()
		for k, v in tuples:
			if k in hashed:
				raise NonUniqException('#__repeated__:{0} old:{1} new:{2}'.format(k, hashed[k], v), k, '..', [hashed[k], v])
			else:
				hashed[k] = v
		return hashed
	
	def now(self):
		return timestamp()
	
	def groupby(self, alist, f):
		hashed = dict()
		for e in alist:
			k = f(e)
			if not k in hashed:
				hashed[k] = list()
			hashed[k].append(e)
		return hashed
	def collect(self, f, alist):
		return self.groupby(f, alist)
	
	def hashby(self, f, alist):
		return self.groupby(alist, f)

	def asdict(self, alist, kf=None, vf=None):
		if not kf: kf = lambda x: x[0]
		if not vf: vf = lambda x: x[1]
		hashed = dict()
		for e in alist:
			k = kf(e)
			if k in hashed:
				raise Exception('__repeatedKey:{0} originalValue:{1} newValue:{2}__'.format(k, hashed[k], vf(e)))
			else:
				hashed[k] = vf(e)
		return hashed		
		
	def by_keyvalue(self, alist, kf=None, vf=None):
		if not kf: kf=lambda x: x
		if not vf: vf=lambda x: x
		hashed = dict()
		for x in alist:
			k = kf(x)
			if not k in hashed:
				hashed[k] = [vf(x)]
			else:
				hashed[k].append(vf(x))
		return hashed

	
	def basename(self, f):
		return os.path.basename(f)
	def fname(self, f):
		return self.basename(f)
	def filename(self, f):
		return self.basename(f)

	def dirname(self, f):
		return os.path.dirname(f)


class Json:
	def __init__(self):
		self.multidict = True
		self.sort_keys = True
		self.indent = 4
		self.separators = (',', ': ')
	def loadf(self, f):
		if self.multidict:
			return self.loadf_multidict(f)
		else:
			with open(f) as target:
				return json.load(target)
	def dumpf(self, f, data):
		stringed = self.pretty(data)
		with open(f, 'w') as outfile:
			outfile.write(stringed)
		return f
	def loadf_multidict(self, f):
		with open(f) as target:
			return self.loads_multidict(target.read())
	def loads_multidict(self, data):
		def multidict_parser(pairs):
			d = defaultdict(list)
			for k, v in pairs:
				d[k].append(v)
			return { k: v[0] if len(v) == 1 else v for k, v in d.items()} 
		return json.JSONDecoder(object_pairs_hook=multidict_parser).decode(data)
	def pretty(self, arg):
		return json.dumps(arg, sort_keys=self.sort_keys, indent=self.indent, separators=self.separators)
	def compact(self, arg):
		return json.dumps(arg, sort_keys=self.sort_keys)
	def pp(self, data, f=None):
		if not f:
			print(self.pretty(data))
		else:
			self.dumpf(f, data) 
	def __call__(self, s):
		return self.pretty(s)
	def copyobj(self, o):
		return self.loads_multidict(self.pretty(o))


class Logger:
	def __init__(self):
		pass
	def __call__(self, m):
		sys.stderr.write('{0}'.format(m))
	def warn(self, m):
		self.__call__(m)


class Console:
	def __init__(self):
		self.a = 1
	def wait(self):
		self.console(self.color("..."))
	def color(self, m, c='green'):
		return m
	def console(self, msg=''):
		return input(msg)
	def pick(self, alist):
		n = len(alist)
		for i, e in enumerate(alist):
			self.log((i, e))
		c = -1
		while not c > -1 and c < n:
			c = self.console('select...?')
			try:
				c = int(c)
			except Exception as err:
				c = -1
		return alist[c]
	def tryuniq(self, alist, f=None):
		try:
			return self.uniq(alist)
		except Exception as err:
			self.log(err)
			if not f:
				f = self.interactive_pick
			return f(alist)	

class OutputFiles:
	def __init__(self):
		pass
	def excel(self, hashedHash, f, transpose=False):
		frame = pandas.DataFrame(hashedHash)
		if transpose:
			frame = frame.transpose()
		frame.to_excel(f)
		return f
	def fexcel(self, f, hashedHash, transpose=False): # because arguments in self.excel are reverse of ususal convention!!!!!
		return self.excel(hashedHash, f, transpose)  
	def dumpf_excel(self, f, hashedHash, transpose=False):
		return self.excel(hashedHash, f, transpose)
	def str_jira(self, hashedHash, keyname='id'):
		fields_no_id  = sorted(list(set([k for v in hashedHash.values() for k in v])))
		fields = [keyname] + sorted(fields_no_id)
		delim, delim2  = '|', '||'
		row = lambda x: '{1}{0}{1}'.format(delim.join([str(e) for e in x]), delim)
		hrow = lambda x: '{1}{0}{1}'.format(delim2.join([str(e) for e in x]), delim2)
		table = [hrow(fields)]
		for k in hashedHash:
			table.append(row([k] + [hashedHash[k][f] for f in fields_no_id]))
		return '\n'.join(table)
		

class LoadFiles:
	def __init__(self):
		pass
	def excel(self, f):
		import pandas
		return pandas.read_excel(f)
	def as_recordlist(self, data):
		top = list(data.keys())
		index = sorted(data[top[0]].keys())
		for k in top:
			assert sorted(data[k].keys()) == index
		return [{ k:data[k][e] for k in top} for e in index]
	def entries(self, f):
		with open(f) as infile:
			return [e.strip() for e in infile.readlines()]




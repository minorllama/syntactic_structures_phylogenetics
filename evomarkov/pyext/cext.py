class Ok:
	class Fail(Exception):
		pass
	@staticmethod
	def fail(trace=None):
		ok = Ok(None)
		ok._ok = False
		ok.trace = trace
		return ok
	def __init__(self, val):
		self._val = val
		self._ok = True
		self.trace = None
	def __bool__(self):
		return self._ok
	@property
	def success(self):
		if self._ok: 
			return self._val
		raise Ok.Fail(Exception("__failure__"))
	def __call__(self):
		return self.success
	def unwrap(self):
		return self.success
	@staticmethod
	def tests():
		a = Ok(1)
		a.success
	def or_else(self, *args):
		if self.__bool__() or len(args) == 0:
			return self.success
		else:
			return args[0]
		
def entry(data, *args):
	d = data
	path = list()
	try:
		for e in args:
			path.append(e)
			d = d[e]
		return Ok(d)
	except Exception as err:
		return Ok.fail({'path' : path, "err" : err})

def listentry(alist, k):
	if k < len(alist):
		return Ok(alist[k]) 
	else:
		return Ok.fail({"index_error":k, "length" : len(alist) })



		
		

def uniq(alist):
	if len(alist) == 1:
		return Ok(alist[0])
	else:
		found = set()
		for e in alist:
			found.add(e)
			if len(found) > 1:
				return Ok.fail({"nonuniq":found})
	foundlist = list(found)
	if len(foundlist) == 0:
		return Ok.fail({"empty":foundlist})
	return Ok(foundlist[0])

def safehash(alist):
	data = dict()
	for k, v in alist:
		if k in data:
			return Ok.fail(trace = {'repeated' : [k, v, data[k]] })
		else:
			data[k] = v
	return Ok(data)

def groupby(alist, kf, vf=None):
	data = dict()
	for e in alist:
		k = kf(e)
		if not k in data: data[k] = list()
		if vf is None:
			data[k].append(e)
		else:
			data[k].append(vf(e))
	return data

def tuplehash(alist):
	return groupby(alist, kf = lambda x: x[0], vf = lambda y: y[1])


def __moduletests():
	assert getpath({1:{2:{3:4}}}, 1, 2, 3)() == 4



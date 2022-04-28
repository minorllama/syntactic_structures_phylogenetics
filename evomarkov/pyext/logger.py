from . import utils 

class Logger2:
	def __init__(self):
		self.log = list()
		self.stream = True
		self.utils  = utils.Utils()
	def __call__(self, e):
		if self.stream:
			print(e)
		self.log.append(e)
	def tbl(self, f=None, delim='\t'):
		if f:
			entries = [delim.join(e) for e in self.log]
			return self.utils.writel(f, entries)	
		else:
			for e in self.log:
				print(delim.join(e))



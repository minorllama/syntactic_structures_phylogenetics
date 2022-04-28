import logging

class Logging:
	def __init__(self, logger=None, name=None):
		if name:
			self.logging = logging.getLogger(name)
		elif logger:
			self.logging = logger
		else:
			self.logging = logging.getLogger()
	def __call__(self, m):
		self.logging.info(m)
		

# Helpers module

import sys
import getopt
import pip

def install_module(package):
	pip.main(['install', package])

def foreach(function, iterable):
	for element in iterable:
		function(element)

def dict_merge(x, y):
	z = x.copy()
	z.update(y)
	return z

def printf(*arg):
	print str(arg)
	sys.stdout.flush()

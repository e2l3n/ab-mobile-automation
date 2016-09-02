#!/usr/bin/python

import sys

from modules.settings import *
from modules.helpers import *
from modules.request_helpers import *
from modules.build import *
from modules.tam_publish import *

# print '---------------------------'
# print 'Number of arguments:', len(sys.argv), 'arguments.'
# print 'Argument List:', str(sys.argv)
# print '---------------------------'

def main(argv):

	settings =  Settings().load_settings(argv)

	upload_tam(settings, { 'Content-Type': 'application/json; charset=UTF-8' }, build(settings))

	printf('DONE')

if __name__ == '__main__':
	main(sys.argv[1:])

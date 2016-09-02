from helpers import *

try:
	import httplib2
except ImportError:
	print 'Installing httplib2 module'
	install_module('httplib2')

import httplib2

def ensure_success_status(resp, content):
	printf('Response Status', resp.status)
	if resp.status > 400:
		printf('Response Content', content)
		quit()

def do_request(url, method, headers=None, body=None):
	http = httplib2.Http()
	resp, content = http.request(url, method=method, headers=headers, body=body)
	ensure_success_status(resp, content)
	return resp, content

def do_post(url, headers, body):
	return do_request(url, 'POST', headers, body)

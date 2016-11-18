import sys
from modules.request_helpers import *

def download_resources(resources):
	http = httplib2.Http()
	printf('Downloading resources ...')
	for r in resources:
		filename = 'undefined'

		if r['type'] == 'device':
			filename = 'device_ios.ipa' if r['platform'] == 'iOS' else 'device_android.apk'
		elif r['type'] == 'simulator' and r['platform'] == 'iOS':
			filename = 'simulator_ios.zip'

		resp, content = http.request(r['url'], "GET")
		with open(filename, 'wb') as f:
			f.write(content)
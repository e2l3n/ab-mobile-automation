#!/usr/bin/python

import sys
import urllib
import json
import glob
from modules.settings import *
from modules.helpers import *
from modules.request_helpers import *

try:
	from urlparse import urlparse
except ImportError:
	from urllib.parse import urlparse

def build(settings):

	__file_path = settings.appid + '.zip';
	__search_patterns = ['../*/'+ __file_path , '../**/*/*/'+ __file_path,'../**/*/'+ __file_path, './**/*/'+ __file_path]

	project_files = []

	for pattern in __search_patterns:
		project_files += glob.glob(pattern)

	printf('Found Package Files - ', project_files)

	headers = {'Authorization': 'ApplicationToken {0}'.format(settings.app_token)}

	printf('Uploading Package ...')
	printf('File - ', project_files[0])

	targetUrl = urlparse('{0}/{1}/projects/importProject/{2}'.format(settings.server_api_url, settings.appid, settings.project_name_url_encoded))
	resp, content = do_post(targetUrl.geturl(), headers=headers, body=open(project_files[0], 'rb'))

	printf('Building ...')

	targetUrl = urlparse('{0}/{1}/build/{2}'.format(settings.server_api_url, settings.appid, settings.project_name_url_encoded))
	resp, content = do_post(targetUrl.geturl(), headers=dict_merge(headers, {'Content-Type': 'application/json'}), body=json.dumps(settings.configuration['build']))

	json_response=json.loads(content)

	if len(json_response['Errors']) > 0:
		print json_response['Errors']
		quit()

	build_result = json_response['ResultsByTarget']['Build']

	resource = list(map(lambda x: { 'url': x['FullPath'], 'platform': x['Platform']}, list(filter(lambda x: x['Disposition'] == 'BuildResult', build_result['Items']))))

	printf('Resources: ', resource)

	return resource

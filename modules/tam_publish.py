import sys
import urllib
import glob
import json
from modules.settings import *
from modules.helpers import *
from modules.request_helpers import *

try:
	from urlparse import urlparse
except ImportError:
	from urllib.parse import urlparse

def upload_tam(settings, headers, resources):

	printf('Authenticating ...')

	targetUrl = urlparse('{0}/appbuilder/Mist/authentication/Login'.format(settings.server_url))
	auth_resp, auth_content = do_post(targetUrl.geturl(), headers={ 'Content-Type' : 'application/x-www-form-urlencoded'}, body='username={0}&password={1}'.format(settings.user, settings.password))

	# At this point, our 'auth_resp' variable contains a dictionary of HTTP header fields that were returned by the login request.
	# If a cookie was returned, you would see a 'set-cookie' field containing the cookie value.
	# We want to take this value and put it into the outgoing HTTP header for our subsequent requests:
	headers['Cookie'] = auth_resp['set-cookie']

	printf('Headers', headers)

	printf('Get Available Applications ...')

	targetUrl = urlparse('{0}/appmanager/api/accounts/{1}/applications'.format(settings.server_url, settings.tam_appid))

	resp, content = do_request(targetUrl.geturl(), 'GET', headers)

	json_response = json.loads(content)

	app_records = filter(lambda x: x['appId'].lower() == settings.app_identifier.lower() and x['version'] == settings.app_version, json_response['result'])

	printf('Publishing {0} ...'.format(settings.app_version))
	if (len(app_records) > 0):
		for r in app_records:
			tam_app_record_id = r['id']
			printf('Unpublish App from TAM', tam_app_record_id)
			targetUrl = urlparse('{0}/appmanager/api/accounts/{1}/applications/{2}/publish'.format(settings.server_url, settings.tam_appid, tam_app_record_id))
			resp, content = do_post(targetUrl.geturl(), headers=headers, body='{"isPublished":false}')

	for r in resources:
		printf('Publish {0} to TAM'.format(r['platform']))
		targetUrl = urlparse('{0}/appbuilder/api/apps/{1}/tam/applications/{2}?packageUri={3}'.format(settings.server_url, settings.appid, settings.project_name_url_encoded, r['url']))
		resp, content = do_post(targetUrl.geturl(), headers=headers, body=json.dumps(settings.configuration['publish']))

import sys
import os
import getopt
import glob
import json
from helpers import *

class Settings:

	appid = ''
	tam_appid = ''
	project_name = ''
	app_token = ''
	user = ''
	password = ''
	server_url = 'https://platform.telerik.com'
	server_api_url = ''
	project_name_url_encoded = ''
	configuration = None,
	startup_file_location = '',
	app_version = '',
	app_identifier = ''

	def print_usage(exitCode):
		print 'build-automation.py -i <appid> -n <project_name> -t <app_token> -c <config> -s <server_url|https://platform.telerik.com>'
		sys.exit(exitCode)

	def load_settings(self, argv):

		self._parse_args(argv);

		if os.path.isfile(self.startup_file_location):
			self._load_from_file(self.startup_file_location);

		self._load_from_project_file(self.project_name)

		printf('Application ID', self.appid)
		printf('Application Token', self.app_token)
		printf('Project Name', self.project_name)
		printf('Server Url', self.server_url)
		printf('TAM ID', self.tam_appid)

		self.server_api_url = '{0}/appbuilder/api/apps/'.format(self.server_url)
		self.project_name_url_encoded = self.project_name.replace(' ', '%20')

		return self;

	def _load_from_project_file(self, project_name):
		# Find ABProject and extract BundleVersion and AppIdentifier
		ab_project_files = filter(lambda x: x.find(project_name) >= 0, glob.glob('../*/.abproject') + glob.glob('../**/*/.abproject') + glob.glob('./**/*/.abproject'))

		printf('Found Project Files: ', ab_project_files)

		ab_project = json.load(open(ab_project_files[0], 'rb'))
		self.app_version = ab_project['BundleVersion']
		self.app_identifier = ab_project['AppIdentifier']

		printf('AppIdentifier', self.app_identifier)
		printf('BundleVersion', self.app_version)

	def _load_from_file(self, startup_file):
		startup_config = json.load(open(startup_file, 'rb'))

		self.appid = startup_config['appid']
		self.project_name = startup_config['project_name']
		self.app_token = startup_config['auth']['app_token']
		self.user = startup_config['auth']['user']
		self.password = startup_config['auth']['password']
		self.configuration = startup_config['configuration']
		self.server_url = startup_config['server_url']
		self.tam_appid = startup_config['tam_appid']

	def _parse_args(self, argv):
		try:
			opts, args = getopt.getopt(argv,'hi:n:t:s:f:',['help','appid=','project_name=','app_token=','server_url=','startup_file='])
		except getopt.GetoptError:
			usage(2)
		for opt, arg in opts:
			if opt in ('-h', '--help'):
				usage(0)
			elif opt in ('-i', '--appid'):
				self.appid = arg
			elif opt in ('-n', '--project_name'):
				self.project_name = arg
			elif opt in ('-t', '--app_token'):
				self.app_token = arg
			elif opt in ('-s', '--server_url'):
				self.server_url = arg
			elif opt in ('-f', '--startup_file'):
				self.startup_file_location = arg

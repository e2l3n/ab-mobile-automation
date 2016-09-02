import sys

def usage(exitCode):
	print 'build-automation.py -i <appid> -n <project_name> -t <app_token> -s <server_url|https://platform.telerik.com>'
	sys.exit(exitCode)

def get_options(argv):
	global appid, project_name, app_token, server_url, server_api_url

	try:
		opts, args = getopt.getopt(argv,'hi:n:t:s:',['help','appid=','project_name=','app_token=','server_url='])
	except getopt.GetoptError:
		usage(2)
	for opt, arg in opts:
		if opt in ('-h', '--help'):
			usage(0)
		elif opt in ('-i', '--appid'):
			appid = arg
		elif opt in ('-n', '--project_name'):
			project_name = arg
		elif opt in ('-t', '--app_token'):
			app_token = arg
		elif opt in ('-s', '--server_url'):
			server_url = arg

	printf('Application ID', appid)
	printf('Application Token', app_token)
	printf('Project Name', project_name)
	printf('Server Url', server_url)

	server_api_url = '{0}/appbuilder/api/apps/'.format(server_url)

	return appid, project_name, app_token, server_url

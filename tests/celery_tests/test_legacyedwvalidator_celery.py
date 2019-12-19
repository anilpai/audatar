"""to test a Validation Check input: classpath and parameters output: vc_status
as "pending" or "success" or "failure"."""

# '''
# Legacy EDW validator
# '''
#
# edw_db_hostname = input("Enter Legacy EDW Host Name: \n (Default: rptdevdb01.homeaway.live ) ")
# edw_db_name = input("Enter Legacy EDW Database Name: \n (Default: DataValidation) ")
# username = input("Enter your HA username: ")
# password = input("Enter your HA password: ")
# vc_name = input("Enter the Validation Check Name: \n (Example: PR_VLD_SiteMissingGoogleAnalyticsAccount ) ")
#
# connection_string = "mssql+pymssql://{0}:{1}@{2}/{3}".format('wvrgroup.internal\\{0}'.format(username), password, edw_db_hostname, edw_db_name)
#
# parameters = {'connection_string': connection_string, 'vc_name': vc_name}
# validator = 'LegacyEDWValidator'
# parameters['class_path'] = validator
#
# r = requests.post("http://localhost:8080/api/runVC", data=json.dumps(parameters, indent=4, default=encode))
# print(r)
# print(r.json())

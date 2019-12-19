# edw_db_hostname = input("Enter Legacy EDW Host Name: \n (Default: rptdevdb01.homeaway.live ) ")
# edw_db_name = input("Enter Legacy EDW Database Name: \n (Default: DataValidation) ")
# username = input("Enter your HA username: ")
# password = input("Enter your HA password: ")
#
# username = 'wvrgroup.internal\\{0}'.format(username)
# connection_string = "mssql+pymssql://{0}:{1}@{2}/{3}".format(username, password, edw_db_hostname, edw_db_name)
#
# vc_name = input("Enter the Validation Check Name: \n (Example: PR_VLD_SiteMissingGoogleAnalyticsAccount ) ")
#
# validator = LegacyEDWValidator({'connection_string': connection_string, 'vc_name': vc_name})
# result = validator.validate()
#
# print("Result")
# print("======")
# print("Status: {}".format(result.status))
# print("Results JSON:")
# print(result.result_records_json())

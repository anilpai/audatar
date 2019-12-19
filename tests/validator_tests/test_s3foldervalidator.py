# aws_access_key_id = input("Enter AWS Access Key Id: ")
# aws_secret_access_key = input("Enter AWS Secret Access Key: ")
# bucket = input("Enter AWS Bucket: ")
# folder = input("Enter AWS Bucket Folder: ")
# connection = AWSConnection({'service':'s3', 'aws_access_key_id': aws_access_key_id, 'aws_secret_access_key': aws_secret_access_key, 'region': 'us-east-1'})
#
# validator = S3FolderValidator({'connection': connection, 'bucket': bucket, 'folder': folder})
# result = validator.validate()
#
# print("Result")
# print("======")
# print("Status: {}".format(result.status))
# print("Results JSON:")
# print(result.result_records_json())

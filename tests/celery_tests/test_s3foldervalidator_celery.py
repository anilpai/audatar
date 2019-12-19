"""to test a Validation Check input: classpath and parameters output: vc_status
as "pending" or "success" or "failure"."""

# S3 Folder validator

# aws_access_key_id = input("Enter AWS Access Key Id: ")
# aws_secret_access_key = input("Enter AWS Secret Access Key: ")
# bucket = input("Enter AWS Bucket: ")
# folder = input("Enter AWS Bucket Folder: ")
#
# parameters = {'service':'s3', 'aws_access_key_id': aws_access_key_id, 'aws_secret_access_key': aws_secret_access_key, 'region': 'us-east-1'}
# parameters['bucket'] = bucket
# parameters['folder'] = folder
# validator = 'S3FolderValidator'
# parameters['class_path'] = validator
#
# r = requests.post("http://localhost:8080/api/runVC", data=json.dumps(parameters, indent=4, default=encode))
# print(r)
# print(r.json())

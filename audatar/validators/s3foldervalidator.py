from audatar.connections import AWSConnection
from audatar.validators import ValidatorBase, ValidationResult
from audatar.ui import ConnectionField, TextField, TextAreaField, SelectField


class S3FolderValidator(ValidatorBase):
    """A validator that checks if an S3 folder exists within a specified bucket
    params: A dictionary including values for following keys:
           connection: AWSConnection 
           bucket: string 
           folder: string
    """

    def __init__(self, input_parameters):
        super().__init__(input_parameters, self.required_parameters())
        parameters = self.parameter_values()
        self.connection = parameters['connection']
        self.bucket = parameters['bucket']
        self.folder = parameters['folder']

    def validate(self):
        result, column_names = None, None
        connector = self.connection.connect()
        result = connector.list_objects(Bucket=self.bucket, Prefix=self.folder)
        column_names = ['result']
        if 'Contents' in result:
            return ValidationResult(ValidationResult.PASS, [{'result': 'Folder: {} exists'.format(self.folder)}], column_names)
        else:
            return ValidationResult(ValidationResult.FAIL, [{'result': 'Folder: {} does NOT exist'.format(self.folder)}], column_names)

    @staticmethod
    def required_parameters():
        return [('connection', AWSConnection), ('bucket', str), ('folder', str)]

    @staticmethod
    def ui_fields():
        connection_field = ConnectionField(parameter_name='connection', label='Connection',
                                           description='Choose an AWS connection', default_value=None, type_filter=['AWS'], name_filter=None)
        bucket_name_field = TextField(parameter_name='bucket', label='Bucket', description='Enter a valid S3 bucket')
        folder_name_field = TextField(parameter_name='folder', label='Folder', description='Enter a valid S3 folder')
        return [connection_field, bucket_name_field, folder_name_field]

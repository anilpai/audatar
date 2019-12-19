import boto3

from audatar.connections import ConnectionBase


class AWSConnection(ConnectionBase):
    def __init__(self, name, parameters):
        super().__init__(name, parameters, self.required_parameters())
        self.__aws_access_key_id = parameters['aws_access_key_id']
        self.__aws_secret_access_key = parameters['aws_secret_access_key']
        self.__service = parameters['service']
        self.__region = parameters['region']

    def connect(self):
        """see: http://boto3.readthedocs.io/en/latest/reference/services/

        :return: returns boto3 client for specified service

        """
        session = boto3.Session(aws_access_key_id=self.__aws_access_key_id,
                                aws_secret_access_key=self.__aws_secret_access_key, region_name=self.__region)
        return session.client(self.__service)

    @staticmethod
    def required_parameters():
        return [('aws_access_key_id', str), ('aws_secret_access_key', str), ('service', str), ('region', str)]

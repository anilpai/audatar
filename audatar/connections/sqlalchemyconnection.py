from sqlalchemy import create_engine
from audatar.connections import ConnectionBase
import json


class SQLAlchemyConnection(ConnectionBase):
    def __init__(self, name, parameters):
        super().__init__(name, parameters, self.required_parameters())
        self.__connection_string = parameters['connection_string']
        self.__connection = None
        if 'connection_args' in parameters:
            self.__connection_args = json.loads(parameters['connection_args'])
        else:
            self.__connection_args = {}

    def connect(self):
        """
        :return: returns SQLAlchemy connection object
        """
        engine = create_engine(self.__connection_string, connect_args=self.__connection_args,
                               pool_size=60, max_overflow=0, pool_recycle=20)
        self.__connection = engine.raw_connection()
        return self.__connection.cursor()

    def close(self):
        self.__connection.close()

    @staticmethod
    def required_parameters():
        return [('connection_string', str)]

    @staticmethod
    def optional_parameters():
        return [('connection_args', str)]

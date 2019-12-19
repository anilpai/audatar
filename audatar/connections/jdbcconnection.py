import ha_jaydebeapi
from audatar.connections import ConnectionBase


class JDBCConnection(ConnectionBase):
    def __init__(self, name, parameters):
        super().__init__(name, parameters, self.required_parameters())
        self.__password = parameters['password']
        self.__jar_path = parameters['jar_path']
        self.__driver_name = parameters['driver_name']
        self.__connection_string = parameters['connection_string']
        self.__connection = None

    def connect(self):
        self.__connection = ha_jaydebeapi.connect(self.__driver_name,
                                                  self.__connection_string,
                                               ['', self.__password], self.__jar_path)
        return self.__connection.cursor()

    def close(self):
        self.__connection.close()

    @staticmethod
    def required_parameters():
        return [('password', str), ('jar_path', str), ('driver_name', str), ('connection_string', str)]

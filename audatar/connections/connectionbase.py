class ConnectionBase:
    def __init__(self, name, parameters, required_params=None):
        self.__parameter_values = parameters
        self.__name = name
        if required_params is not None:
            for name, typ in required_params:
                if name not in self.__parameter_values:
                    raise AttributeError('{0} is a required parameter and it was not found.'.format(name))
                elif not isinstance(self.__parameter_values[name], typ):
                    raise ValueError('{0} parameter is expected to be of type {1}'.format(name, typ.__name__))

    def connect(self):
        raise NotImplementedError

    def parameter_values(self):
        return self.__parameters_values

    @staticmethod
    def required_parameters():
        """In child classes this should return a list of tuples that represent
        connection parameters that are required (parameter name/key, class)"""
        raise NotImplementedError

    @staticmethod
    def optional_parameters():
        """In child classes this should return a list of tuples that represent
        connection parameters that are optional (parameter name/key, class)"""
        return []

    def __repr__(self):
        return self.__name

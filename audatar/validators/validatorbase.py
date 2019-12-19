class ValidatorBase:
    def __init__(self, input_parameters, required_params=None):
        self.__parameter_values = input_parameters
        if required_params is not None:
            for name, typ in required_params:
                if isinstance(typ, list):
                    typ = tuple(typ)
                if name not in self.__parameter_values:
                    raise AttributeError(
                        '{0} is a required parameter and it was not found.'.format(name))
                elif not isinstance(self.__parameter_values[name], typ):
                    raise ValueError(
                        '{0} parameter is expected to be of type {1}'.format(name, typ.__name__))

    def parameter_values(self):
        return self.__parameter_values

    def validate(self):
        raise NotImplementedError
        
    def metric(self):
       raise NotImplementedError

    def input_errors(self):
        return None

    def fields(self):
        return None

    @staticmethod
    def required_parameters():
        raise NotImplementedError

    @staticmethod
    def optional_parameters():
        return []

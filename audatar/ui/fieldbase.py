class FieldBase:
    def __init__(self, parameter_name, label, description=None, default_value=None):
        self.__parameter_name = parameter_name
        self.__label = label
        self.__description = description
        self.__default_value = default_value

    def parameter_name(self):
        return self.__parameter_name

    def label(self):
        return self.__label

    def description(self):
        return self.__description

    def default_value(self):
        return self.__default_value

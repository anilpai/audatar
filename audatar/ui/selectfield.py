from audatar.ui.fieldbase import FieldBase


class SelectField(FieldBase):
    def __init__(self, parameter_name, label, description, selection_list=None, allow_multiple=False):
        super().__init__(parameter_name, label, description)
        self.__selection_list = selection_list
        self.__allow_multiple = allow_multiple

    def allow_multiple(self):
        return self.__allow_multiple

    def selection_list(self):
        return self.__selection_list

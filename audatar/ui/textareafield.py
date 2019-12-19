from audatar.ui.fieldbase import FieldBase


class TextAreaField(FieldBase):
    def __init__(self, parameter_name, label, description, rows=5, placeholder=None, default_value=None):
        super().__init__(parameter_name, label, description, default_value)
        self.__rows = rows
        self.__placeholder = placeholder

    def rows(self):
        return self.__rows

    def placeholder(self):
        return self.__placeholder

from audatar.ui.fieldbase import FieldBase


class TextField(FieldBase):
    def __init__(self, parameter_name, label, description, default_value=None):
        super().__init__(parameter_name, label, description, default_value)

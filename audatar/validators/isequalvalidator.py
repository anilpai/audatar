from audatar.validators import ValidatorBase, ValidationResult
#from audatar.ui import ConnectionField, TextField, TextAreaField, SelectField


class IsEqualValidator(ValidatorBase):
    """A an EXAMPLE validator that checks to see if all values within a
    dictionary are equal. This validator will not exist in the actual Audatar
    application for use.

    :param input: A dictionary with key/value pairs
    """

    def __init__(self, input_parameters):
        super().__init__(input_parameters)

    def validate(self):
        input_params = self.input_parameters()
        result = None

        i = 0
        prev_value = None
        for key, value in input_params.items():
            if i == 0:
                prev_value = value
            elif value != prev_value:
                result = input_params
                result['Result'] = 'Fail: Values are not equal'
                return ValidationResult(ValidationResult.FAIL, [result], sorted(list(input_params.keys()))).result_records_json()
            else:
                prev_value = value
            i += 1

        result = input_params
        result['Result'] = 'Pass: Values are equal'
        return ValidationResult(ValidationResult.PASS, [result], sorted(list(input_params.keys()))).result_records_json()

    """
    @staticmethod
    def ui_fields():
        connection_field = SelectField(parameter_name = 'parameter_name', label='label', description='description', selection_list=[('=','<=','>=','<','>','!=')])
        return [connection_field]
    """

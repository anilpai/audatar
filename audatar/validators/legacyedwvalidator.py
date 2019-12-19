from audatar.validators import ValidatorBase, ValidationResult
from audatar.connections import SQLAlchemyConnection
from audatar.ui import ConnectionField, TextField, TextAreaField, SelectField
from audatar.utils import helper
import logging

import sys
from audatar.utils.exceptions import JError

logger = logging.getLogger('audatar')


class LegacyEDWValidator(ValidatorBase):
    """A validator that runs the legacy EDW validation engine stored procedures
    on MSSQL Server.

    :param param: Name of a stored procedure.
    """

    def __init__(self, input_parameters):
        super().__init__(input_parameters, self.required_parameters())
        parameters = self.parameter_values()
        self.connection = parameters['connection']
        self.vc_name = parameters['vc_name']

    def validate(self):
        result, column_names = None, None
        cursor = self.connection.connect()

        query = "declare @queryout varchar(max) \
                        execute PR_ValidationCheckEngineAudatar1 \
                        @SingleProcedureName='{0}', @query=@queryout output".format(self.vc_name)
        try:
            cursor.execute(query)

            data = None
            try:
                data = cursor.fetchall()
            except Exception as e:
                logger.info(helper.generate_logging_message('audatar', 'legacyedwvalidator', '', '', 'error', str(e)))
                exc_type, exc_value, exc_trace = sys.exc_info()
                raise JError("%s: %s" % (exc_type, exc_value)).with_traceback(exc_trace)
            finally:
                self.connection.close()
                cursor.close()

            if data:
                column_names = [i[0] for i in cursor.description]

                result = [dict(zip(column_names, row)) for row in data]

            else:
                result = [{'output': 'query return no result'}]
                column_names = ['output']
        except Exception as e:
            logger.info(helper.generate_logging_message('audatar', 'legacyedwvalidator', '', '', 'error', str(e)))
            exc_type, exc_value, exc_trace = sys.exc_info()
            raise JError("%s: %s" % (exc_type, exc_value)).with_traceback(exc_trace)
        finally:
            self.connection.close()
            cursor.close()

        if result == [{'output': 'query return no result'}]:
            return ValidationResult(ValidationResult.PASS, result, column_names)
        else:
            return ValidationResult(ValidationResult.FAIL, result, column_names)

    @staticmethod
    def required_parameters():
        return [('connection', SQLAlchemyConnection), ('vc_name', str)]

    @staticmethod
    def ui_fields():
        connection_field = ConnectionField(parameter_name='connection', label='Connection', description='This should always be EDW_MSSQL', type_filter=None, name_filter=[
                                           'EDW MSSQL DEV', 'EDW MSSQL STAGE', 'EDW MSSQL PROD'], default_value=None)
        validation_check_name_field = TextField(parameter_name='vc_name', label='Validation Check Procedure',
                                                description='This should be a valid ProcedureName in DataValidation.dbo.ValidationCheck')
        return [connection_field, validation_check_name_field]

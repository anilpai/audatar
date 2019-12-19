from audatar.validators import ValidatorBase, ValidationResult
from audatar.connections import SQLAlchemyConnection, JDBCConnection
from audatar.ui import ConnectionField, TextField, TextAreaField, SelectField
from jpype import JException, JavaException, java
from audatar.utils import helper
import logging
import json

import sys
from audatar.utils.exceptions import JError, convert_result_list

logger = logging.getLogger('audatar')


class SqlDataValidator(ValidatorBase):
    """A validator that execute sql query
    param : sql query, result_condition
    """

    def __init__(self, input_parameters):
        super().__init__(input_parameters, self.required_parameters())
        parameters = self.parameter_values()
        self.connection = parameters['connection']
        self.query = parameters['query']
        self.condition = parameters['pass_condition']
        self.data = 0

    def validate(self):
        result, column_names, cursor = None, None, None
        try:
            try:
                cursor = self.connection.connect()
                cursor.execute(self.query)
                self.data = cursor.fetchall()
                column_names = [i[0] for i in cursor.description]
                res = [dict(zip(column_names, row)) for row in self.data]
                result = convert_result_list(res)
            except Exception as e:
                logger.info(helper.generate_logging_message('audatar', 'sqldatavalidator', '', '', 'error', str(e)))
                exc_type, exc_value, exc_trace = sys.exc_info()
                raise JError("%s: %s" % (exc_type, exc_value)).with_traceback(exc_trace)
            finally:
                cursor.close()
                self.connection.close()
        except JavaException as e:
            logger.info(helper.generate_logging_message('audatar', 'sqldatavalidator', '', '', 'error', str(e)))
            exc_type, exc_value, exc_trace = sys.exc_info()
            raise JError("%s: %s" % (exc_type, exc_value)).with_traceback(exc_trace)
        except JException(java.lang.RuntimeException) as ex:
            logger.info(helper.generate_logging_message('audatar', 'sqldatavalidator', '', '', 'error', str(ex)))
            exc_type, exc_value, exc_trace = sys.exc_info()
            raise JError("%s: %s" % (exc_type, exc_value)).with_traceback(exc_trace)
        if len(self.data) == 0:
            result = [{'output': 'query return no result'}]
            column_names = ['output']
        pass_condition = self.condition
        metricdic = {'result_count': len(self.data)}
        if pass_condition == 'query returns no results':
            if len(self.data) != 0:
                logger.info(helper.generate_logging_message('audatar', 'sqldatavalidator', '', '', 'result',
                                                            ValidationResult(ValidationResult.FAIL, result,
                                                                             column_names).result_records_json()))
                return ValidationResult(ValidationResult.FAIL, result, column_names, metricdic)
            else:
                logger.info(helper.generate_logging_message('audatar', 'sqldatavalidator', '', '', 'result',
                                                            ValidationResult(ValidationResult.PASS, result,
                                                                             column_names).result_records_json()))
                return ValidationResult(ValidationResult.PASS, result, column_names, metricdic)

        else:
            if len(self.data) == 0:
                logger.info(helper.generate_logging_message('audatar', 'sqldatavalidator', '', '', 'result',
                                                            ValidationResult(ValidationResult.FAIL, result,
                                                                             column_names).result_records_json()))
                return ValidationResult(ValidationResult.FAIL, result, column_names, metricdic)
            else:
                logger.info(helper.generate_logging_message('audatar', 'sqldatavalidator', '', '', 'result',
                                                            ValidationResult(ValidationResult.PASS, result,
                                                                             column_names).result_records_json()))
                return ValidationResult(ValidationResult.PASS, result, column_names, metricdic)
                
    

    @staticmethod
    def required_parameters():
        return [('connection', [SQLAlchemyConnection, JDBCConnection]), ('query', str), ('pass_condition', str)]

    @staticmethod
    def ui_fields():
        connection_field = ConnectionField(parameter_name='connection', label='Connection', description='Choose a connection', type_filter=[
                                           'SQLAlchemy', 'JDBC'], name_filter=None, default_value=None)
        query_field = TextAreaField(parameter_name='query', label='Query',
                                    description='Enter a valid SQL query', rows=20, default_value=None, placeholder='Please limit the number of results returned in your sql query and do not use select * .')
        condition_field = SelectField(parameter_name='pass_condition', label='Pass Condition', description='Pass on whether the query returns any results or not', selection_list=[
                                      ('query returns no results', 'query returns no results'), ('query returns results', 'query returns results')], allow_multiple=False)
        return [connection_field, query_field, condition_field]

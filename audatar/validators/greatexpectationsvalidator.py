import json
from audatar.validators import ValidatorBase, ValidationResult
from audatar.connections import SQLAlchemyConnection, JDBCConnection
from jpype import JException, JavaException, java
from audatar.ui import ConnectionField, TextAreaField
import pandas as pd
import great_expectations as ge
import great_expectations.dataset as dataset
import logging
from audatar.utils import helper
from great_expectations import util
from types import FunctionType
from inspect import signature

import sys
from audatar.utils.exceptions import JError

logger = logging.getLogger('audatar')


class GreatExpectationsValidator(ValidatorBase):
    """A validator that validates expectations defined by Great Expectations library.
    """
    def __init__(self, input_parameters):
        super().__init__(input_parameters, self.required_parameters())
        parameters = self.parameter_values()
        self.connection = parameters['connection']
        self.query = parameters['query']
        self.expectations = parameters['expectations']

    def validate(self):
        result = []
        column_names = ['Function_Name', 'Parameters', 'Result']
        cursor = None
        try:
            try:
                cursor = self.connection.connect()
                cursor.execute(self.query)
                df = pd.DataFrame(cursor.fetchall())
                df.columns = [i[0] for i in cursor.description]
                df = util._convert_to_dataset_class(df, dataset.pandas_dataset.PandasDataset)
                e = json.loads(self.expectations.replace("'", "\""))

                all_expectations = self.get_all_expectations()
                expectations_list = e['expectations']
                result = []
                flags = []
                for i, e in enumerate(expectations_list):
                    f = list(e.keys())[0]
                    p_list = all_expectations[f]
                    row = {}
                    params = {}
                    for p in p_list:
                        if p in e[f]:
                            params[p] = e[f][p]

                    e_result = getattr(df, f)(**params)

                    row['Function_Name'] = f
                    row['Parameters'] = e[f]
                    row['Result'] = str(e_result['success'])
                    result.append(row)
                    flags.append(e_result['success'])

            except Exception as e:
                logger.info(helper.generate_logging_message('audatar', 'greatexpectationsvalidator', '', '', 'error', str(e)))
                exc_type, exc_value, exc_trace = sys.exc_info()
                raise JError("%s: %s" % (exc_type, exc_value)).with_traceback(exc_trace)
            finally:
                cursor.close()
                self.connection.close()
        except JavaException as e:
            logger.info(helper.generate_logging_message('audatar', 'greatexpectationsvalidator', '', '', 'error', str(e)))
            exc_type, exc_value, exc_trace = sys.exc_info()
            raise JError("%s: %s" % (exc_type, exc_value)).with_traceback(exc_trace)
        except JException(java.lang.RuntimeException) as ex:
            logger.info(helper.generate_logging_message('audatar', 'greatexpectationsvalidator', '', '', 'error', str(ex)))
            exc_type, exc_value, exc_trace = sys.exc_info()
            raise JError("%s: %s" % (exc_type, exc_value)).with_traceback(exc_trace)

        if all(flags):
            return ValidationResult(ValidationResult.PASS, result, column_names)
        else:
            return ValidationResult(ValidationResult.FAIL, result, column_names)

    @staticmethod
    def required_parameters():
        return [('connection', [SQLAlchemyConnection, JDBCConnection]), ('query', str), ('expectations', str)]

    @staticmethod
    def ui_fields():
        connection_field = ConnectionField(parameter_name='connection', label='Connection',
                                           description='Choose a connection',
                                           type_filter=['SQLAlchemy', 'JDBC'],
                                           name_filter=None, default_value=None)
        query_field = TextAreaField(parameter_name='query', label='Query', description='Enter a valid SQL query',
                                    rows=20, default_value=None,
                                    placeholder='Please limit the number of results returned in your sql query and '
                                                'do not use select * .')
        expectations_field = TextAreaField(parameter_name='expectations', label='Expectations',
                                           description='Enter a valid expectation JSON', rows=20, default_value=None,
                                           placeholder='Please make sure the JSON is valid. (Use jsonparseronline.com)')
        return [connection_field, query_field, expectations_field]

    @staticmethod
    def get_all_expectations():
        o = ge.dataset.base.Dataset
        return {x: [s.split('=')[0].lstrip() for s in str(signature(getattr(o, x))).split(',')[1:]] for x, y in
                o.__dict__.items() if type(y) == FunctionType and x.startswith('expect_')}


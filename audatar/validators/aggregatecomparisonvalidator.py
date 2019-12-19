from audatar.validators import ValidatorBase, ValidationResult
from audatar.connections import SQLAlchemyConnection,  JDBCConnection
from audatar.ui import ConnectionField, TextField, TextAreaField, SelectField
from jpype import JException, JavaException, java
from audatar.utils import helper
import logging
import json

import sys
from audatar.utils.exceptions import JError, convert_tuple

logger = logging.getLogger('audatar')


class AggregateComparisonValidator(ValidatorBase):
    """A validator that checks conditions of of 2 aggregate functions between 2
    different sources.

    -    :param connection1: connection to first source.
    -           connection2: connection to second source.
    -           comparison_operator: comparison operator
    -           tolerance_percentage: tolerance percentage
    -           table1: first table name
    -           table2: second table name
    -           table1_predicates: first table predicates
    -           table2_predicates: second table predicates
    -           aggregate1: first table aggregate
    -           aggregate2: second table aggregate
    """

    def __init__(self, input_parameters):
        super().__init__(input_parameters, self.required_parameters())
        parameters = self.parameter_values()
        self.comparison_operator = parameters.get('comparison_operator', None)
        self.table1 = parameters.get('table1', None)
        self.table2 = parameters.get('table2', None)
        self.tolerance_percentage = parameters.get('tolerance_percentage', '')
        self.table1_predicates = parameters.get('table1_predicates', '')
        self.table2_predicates = parameters.get('table2_predicates', '')
        self.connection1 = parameters.get('connection1', None)
        self.connection2 = parameters.get('connection2', None)
        self.aggregate1 = parameters.get('aggregate1', None)
        self.aggregate2 = parameters.get('aggregate2', None)
        self.data_a = 0
        self.data_b = 0

    def validate(self):
        result, column_names, data_a, data_b, output = (None,) * 5
        cursor1 = self.connection1.connect()
        cursor2 = self.connection2.connect()
        if self.tolerance_percentage == '':
            self.tolerance_percentage = '0'
        tolerance_percentage = int(self.tolerance_percentage)
        tolerance_percentage = tolerance_percentage/100

        try:

            query_a = 'select {0} cnt from {1} '.format(self.aggregate1, self.table1) if self.table1_predicates == '' else \
                'select {0} cnt from {1} where {2}'.format(self.aggregate1, self.table1, self.table1_predicates)

            try:
                cursor1.execute(query_a)
                self.data_a = convert_tuple(cursor1.fetchone())[0]
            except Exception as e:
                logger.info(helper.generate_logging_message(
                    'audatar', 'aggregatecomparisonvalidator', '', '', 'error', str(e)))
                exc_type, exc_value, exc_trace = sys.exc_info()
                raise JError("%s: %s" % (exc_type, exc_value)).with_traceback(exc_trace)
            finally:
                self.connection1.close()
                cursor1.close()

            query_b = 'select {0} cnt from {1} '.format(self.aggregate2, self.table2) if self.table2_predicates == '' else \
                'select {0} cnt from {1} where {2}'.format(self.aggregate2, self.table2, self.table2_predicates)

            try:
                cursor2.execute(query_b)
                self.data_b = convert_tuple(cursor2.fetchone())[0]
            except Exception as e:
                logger.info(helper.generate_logging_message(
                    'audatar', 'aggregatecomparisonvalidator', '', '', 'error', str(e)))
                exc_type, exc_value, exc_trace = sys.exc_info()
                raise JError("%s: %s" % (exc_type, exc_value)).with_traceback(exc_trace)
            finally:
                self.connection2.close()
                cursor2.close()

        except JavaException as e:
            logger.info(helper.generate_logging_message(
                'audatar', 'aggregatecomparisonvalidator', '', '', 'error', str(e)))
            exc_type, exc_value, exc_trace = sys.exc_info()
            raise JError("%s: %s" % (exc_type, exc_value)).with_traceback(exc_trace)
        except JException(java.lang.RuntimeException) as ex:
            logger.info(helper.generate_logging_message(
                'audatar', 'aggregatecomparisonvalidator', '', '', 'error', str(ex)))
            exc_type, exc_value, exc_trace = sys.exc_info()
            raise JError("%s: %s" % (exc_type, exc_value)).with_traceback(exc_trace)

        if self.comparison_operator == '=':
            output = 'passed' if (self.data_a - (self.data_a * tolerance_percentage)) <= self.data_b <= (self.data_a +
                                                                                          (self.data_a * tolerance_percentage)) else 'failed'
        elif self.comparison_operator == '>=':
            output = 'passed' if self.data_a >= self.data_b else 'failed'
        elif self.comparison_operator == '<=':
            output = 'passed' if self.data_a <= self.data_b else'failed'
        elif self.comparison_operator == '>':
            output = 'passed' if self.data_a > self.data_b else 'failed'
        elif self.comparison_operator == '<':
            output = 'passed' if self.data_a < self.data_b else 'failed'
        elif self.comparison_operator == '!=':
            output = 'passed' if self.data_a != self.data_b else 'failed'

        results = [{'table name': self.table1, 'aggregate result': self.data_a},
                   {'table name': self.table2, 'aggregate result': self.data_b}]
        column_names = ['table name', 'aggregate result']
        metricdic = {self.table1+'_count' : self.data_a,self.table2+'_count': self.data_b}

        return ValidationResult(ValidationResult.PASS, results, column_names, metricdic) if output == 'passed' else \
            ValidationResult(ValidationResult.FAIL, results, column_names, metricdic)
    

    @staticmethod
    def required_parameters():
        return [('connection1', [SQLAlchemyConnection, JDBCConnection]), ('connection2', [SQLAlchemyConnection, JDBCConnection]), ('table1', str), ('aggregate1', str), ('table2', str), ('aggregate2', str), ('comparison_operator', str)]

    @staticmethod
    def optional_parameters():
        return [('tolerance_percentage', str), ('table1_predicates', str), ('table2_predicates', str)]

    @staticmethod
    def ui_fields():
        connection_field1 = ConnectionField(parameter_name='connection1', label='Connection 1',
                                            description='Choose the connection of the first table for comparison', default_value=None, type_filter=['SQLAlchemy', 'JDBC'], name_filter=None)
        aggregate_table_1 = TextField(parameter_name='aggregate1', label='Aggregate Function table 1',
                                      description='Enter a aggregate function. Example COUNT_BIG, SUM, MAX, MIN')
        connection_table_name_1 = TextField(parameter_name='table1', label='Table 1',
                                            description='Enter the table name from the data source in Connection 1 for comparison')
        predicate_table_1 = TextAreaField(parameter_name='table1_predicates', label='Table 1 Predicates',
                                          description='Enter the predicates (filter conditions) for Table 1 (should be written like a WHERE clause but without using the word WHERE)', rows=5, placeholder=None)
        connection_field2 = ConnectionField(parameter_name='connection2', label='Connection 2',
                                            description='Choose the connection of the second table for comparison', default_value=None, type_filter=['SQLAlchemy', 'JDBC'], name_filter=None)
        aggregate_table_2 = TextField(parameter_name='aggregate2', label='Aggregate Function table 2',
                                      description='Enter a aggregate function. Example COUNT_BIG, SUM, MAX, MIN')
        connection_table_name_2 = TextField(parameter_name='table2', label='Table 2',
                                            description='Enter the table name from the data source in Connection 2 for comparison')
        predicate_table_2 = TextAreaField(parameter_name='table2_predicates', label='Table 2 Predicates',
                                          description='Enter the predicates (filter conditions) for Table 1 (should be written like a WHERE clause but without using the word WHERE)', rows=5, placeholder=None)
        comparison_operator = SelectField(parameter_name='comparison_operator', label='Comparison Operator', description='Choose the comparison operator (Table 1 ? Table 2)', selection_list=[
                                          ('=', '='), ('<=', '<='), ('>=', '>='), ('<', '<'), ('>', '>'), ('!=', '!=')])
        tolerance_percentage = TextField(parameter_name='tolerance_percentage', label='Tolerance Percentage',
                                         description='Enter a tolerence percentage (only applicable if selecting the = operator) as an integer. Example: 2')
        return[connection_field1, aggregate_table_1, connection_table_name_1, predicate_table_1, connection_field2, aggregate_table_2, connection_table_name_2, predicate_table_2, comparison_operator, tolerance_percentage]

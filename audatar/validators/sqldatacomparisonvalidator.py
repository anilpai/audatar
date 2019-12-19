import itertools
from audatar.validators import ValidatorBase, ValidationResult
from audatar.connections import SQLAlchemyConnection, JDBCConnection
from audatar.ui import ConnectionField, TextField, TextAreaField, SelectField
from jpype import JException, JavaException, java
from audatar.utils import helper
import logging

import sys
from audatar.utils.exceptions import JError, convert_result_list

logger = logging.getLogger('audatar')


class SQLDataComparisonValidator(ValidatorBase):
    """A validator that compares data between 2 different sources.

    -    :param connection1: connection to first source.
    -           connection2: connection to second source.
    -           pass_condition: pass condition
    -           query1: first query
    -           query2: second query
    -           query1_key: key from query1
    -           query2_key: key from query2
    -           tolerance_percentage: comma separated list of tolerance percentage
    -           field_name: comma separated list of field name for tolerance
    """

    def __init__(self, input_parameters):
        super().__init__(input_parameters, self.required_parameters())
        parameters = self.parameter_values()
        self.connection1 = parameters['connection1']
        self.connection2 = parameters['connection2']
        self.query1 = parameters['query1']
        self.query1 = parameters['query1']
        self.query1_key = parameters['query1_key']
        self.query2 = parameters['query2']
        self.query2_key = parameters['query2_key']
        self.pass_condition = parameters['pass_condition']
        self.tolerance_percentage = parameters.get('tolerance_percentage', '')
        self.field_name = parameters.get('field_name', '')
        self.data = 0

    def validate(self):
        result, column_names = None, None
        field_name_list, tolerance_percentage_list = None, None
        cursor1, cursor2 = None, None
        tolerance_list = []
        try:
            cursor1 = self.connection1.connect()
            cursor2 = self.connection2.connect()
        except Exception as e:
            self.connection1.close()
            self.connection2.close()
            cursor1.close()
            cursor2.close()
            logger.info(helper.generate_logging_message(
                    'audatar', 'sqldatacomparisonvalidator', '', '', 'error', str(e)))
            exc_type, exc_value, exc_trace = sys.exc_info()
            raise JError("%s: %s" % (exc_type, exc_value)).with_traceback(exc_trace)

        if self.field_name != '':
            field_name_list = (list(map(str.strip, self.field_name.split(','))))

        if self.tolerance_percentage != '':
            tolerance_percentage_list = (list(map(str.strip, self.tolerance_percentage.split(','))))

        if self.field_name != '':
            if len(field_name_list) != len(tolerance_percentage_list):
                result = [{'output': 'Different number of elements in list of field names and tolerance percentage'}]
                column_names = ['output']
                return ValidationResult(ValidationResult.FAIL, result, column_names)

            for index, item in enumerate(field_name_list):
                dictionary = {}
                dictionary['field'] = field_name_list[index]

                dictionary['tolerance'] = (int(tolerance_percentage_list[index])/100)
                tolerance_list.append(dictionary)

        try:
            # Getting data from query 1
            try:
                cursor1.execute(self.query1)
                data1 = cursor1.fetchall()
                column_names1 = [i[0] for i in cursor1.description]
                result1 = convert_result_list([dict(zip(column_names1, row)) for row in data1])
            except Exception as e:
                logger.info(helper.generate_logging_message(
                    'audatar', 'sqldatacomparisonvalidator', '', '', 'error', str(e)))
                exc_type, exc_value, exc_trace = sys.exc_info()
                raise JError("%s: %s" % (exc_type, exc_value)).with_traceback(exc_trace)
            finally:
                self.connection1.close()
                cursor1.close()

            # Getting data from query 2
            try:
                cursor2.execute(self.query2)
                data2 = cursor2.fetchall()
                column_names2 = [i[0] for i in cursor2.description]
                result2 = convert_result_list([dict(zip(column_names2, row)) for row in data2])
            except Exception as e:
                logger.info(helper.generate_logging_message(
                    'audatar', 'sqldatacomparisonvalidator', '', '', 'error', str(e)))
                exc_type, exc_value, exc_trace = sys.exc_info()
                raise JError("%s: %s" % (exc_type, exc_value)).with_traceback(exc_trace)
            finally:
                self.connection2.close()
                cursor2.close()
        except JavaException as e:
            logger.info(helper.generate_logging_message(
                'audatar', 'sqldatacomparisonvalidator', '', '', 'error', str(e)))
            exc_type, exc_value, exc_trace = sys.exc_info()
            raise JError("%s: %s" % (exc_type, exc_value)).with_traceback(exc_trace)
        except JException(java.lang.RuntimeException) as ex:
            logger.info(helper.generate_logging_message(
                'audatar', 'sqldatacomparisonvalidator', '', '', 'error', str(ex)))
            exc_type, exc_value, exc_trace = sys.exc_info()
            raise JError("%s: %s" % (exc_type, exc_value)).with_traceback(exc_trace)

        # Validate keys and column_names
        if self.query1_key not in column_names1:
            result = [{'output': 'key1 not found in column_names in data 1'}]
            column_names = ['output']
            return ValidationResult(ValidationResult.FAIL, result, column_names)

        if self.query2_key not in column_names2:
            result = [{'output': 'key2 not found in column_names in data 2'}]
            column_names = ['output']
            return ValidationResult(ValidationResult.FAIL, result, column_names)

        if self.field_name != '':
            for element in tolerance_list:
                if element['field'] not in column_names1:
                    result = [{'output': 'field name not found in column_names in data 1'}]
                    column_names = ['output']
                    return ValidationResult(ValidationResult.FAIL, result, column_names)

                if element['field'] not in column_names2:
                    result = [{'output': 'field name not found in column_names in data 2'}]
                    column_names = ['output']
                    return ValidationResult(ValidationResult.FAIL, result, column_names)

        # make key in data 2 equal to key in data 1, if they are different,
        if not(self.query1_key == self.query2_key):
            for item in result2:
                item[self.query1_key] = item.pop(self.query2_key)
            for n, i in enumerate(column_names2):
                if i == self.query2_key:
                    column_names2[n] = self.query1_key
            self.query2_key = self.query1_key

        # validate if both queries result have same columns
        temp2 = [x for x in column_names1 if x not in set(column_names2)]
        if temp2:
            result = [{'output': 'No same columns in data 1 and data 2'}]
            column_names = ['output']
            return ValidationResult(ValidationResult.FAIL, result, column_names)

        # VALIDATE DUPLICATES
        all_key_values1 = []
        counter_list1 = []
        all_key_values2 = []
        counter_list2 = []

        # Set number of records by key for data1
        for element in result1:
            new_dict4 = {}
            all_key_values1.append(element[self.query1_key])
            key_elements = [k[self.query1_key] for k in result1 if k.get(
                self.query1_key) and k.get(self.query1_key) == element[self.query1_key]]
            new_dict4[element[self.query1_key]] = len(key_elements)
            counter_list1.append(new_dict4)
        records_by_key1 = [dict(t) for t in set([tuple(d.items()) for d in counter_list1])]

        # Set number of records by key for data2
        for element in result2:
            new_dict4 = {}
            all_key_values2.append(element[self.query2_key])
            key_elements = [k[self.query2_key] for k in result2 if k.get(
                self.query2_key) and k.get(self.query2_key) == element[self.query2_key]]
            new_dict4[element[self.query2_key]] = len(key_elements)
            counter_list2.append(new_dict4)
        records_by_key2 = [dict(t) for t in set([tuple(d.items()) for d in counter_list2])]

        # Records that match
        intersec2 = [item for item in all_key_values1 if item in all_key_values2]

        # Find key counts that do not match
        for item in intersec2:
            for index, dict1 in enumerate(records_by_key1):
                if item in dict1.keys():
                    comp1 = dict1.get(item)
            for index, dict2 in enumerate(records_by_key2):
                if item in dict2.keys():
                    comp2 = dict2.get(item)
            if not (comp1 == comp2):
                # if count does not match, send to Fail
                result = [{'output': 'Count by key does not match.'}]
                column_names = ['output']
                return ValidationResult(ValidationResult.FAIL, result, column_names)

        # Validate results
        intersec = [item for item in result1 if item in result2]
        sym_diff = [item for item in itertools.chain(result1, result2) if item not in intersec]

        if not sym_diff:
            result = [{'output': 'Queries matched'}]
            column_names = ['output']
            return ValidationResult(ValidationResult.PASS, result, column_names)

        # list of different keys
        list_to_convert = []
        for index, dict1 in enumerate(sym_diff):
            for key in dict1:
                if key == self.query1_key or key == self.query2_key:
                    list_to_convert.append(dict1[key])
        column_names = set().union(*(d.keys() for d in sym_diff))

        # final list of keys from different records
        list_final = list(set(list_to_convert))
        # final list for validation result data
        final_list = []
        # list of column names in order
        order_list = []
        order_list.append('key')

        # for each record in list, find values in data 1 and data 2 and format values in one dict
        for ind, value in enumerate(list_final):
            new_dict = {}
            new_dict['key'] = value
            flag1 = False
            flag2 = False
            for col in column_names:
                if not (col == self.query1_key or col == self.query2_key):

                    # Data 1
                    new_value = 'None'
                    new_dict2 = {}
                    new_key = 'query1_'+col
                    if not(new_key in order_list):
                        order_list.append(new_key)
                    for index, dict1 in enumerate(result1):
                        if(dict1 not in intersec):
                            if(dict1.get(self.query1_key) == value):
                                for key in dict1:
                                    if(key == col):
                                        new_value = str(dict1[key])
                                        flag1 = True
                    new_dict2[new_key] = new_value
                    new_dict.update(new_dict2)

                    # Data 2
                    new_value = 'None'
                    new_dict2 = {}
                    new_key = 'query2_'+col
                    if not(new_key in order_list):
                        order_list.append(new_key)
                    for index, dict2 in enumerate(result2):
                        if dict2 not in intersec:
                            if dict2.get(self.query2_key) == value:
                                for key in dict2:
                                    if key == col:
                                        new_value = str(dict2[key])
                                        flag2 = True
                    new_dict2[new_key] = new_value
                    new_dict.update(new_dict2)

            if self.pass_condition == 'Query 1 and Query 2 data is the same for all rows that join in both queries':
                if flag1 and flag2:
                    final_list.append(new_dict)
            else:
                final_list.append(new_dict)

        if self.field_name != '':
            for i in final_list:
                for element in tolerance_list:
                    if i['query1_'+element['field']] != 'None' and i['query2_'+element['field']] != 'None':
                        output = 'passed' if float(i['query1_' + element['field']]) - \
                                             (float(i['query1_' + element['field']]) * element['tolerance']) <= \
                                             float(i['query2_' + element['field']]) <= \
                                             float(i['query1_' + element['field']]) + \
                                             (float(i['query1_' + element['field']]) * element['tolerance']) else 'failed'

                        if output == 'failed':
                            result = final_list
                            column_names = order_list
                            return ValidationResult(ValidationResult.FAIL, result, column_names)
                        else:
                            result = [{'output': 'Queries matched'}]
                            column_names = ['output']
        else:
            if final_list:
                result = final_list
                column_names = order_list
            else:
                result = [{'output': 'Queries matched'}]
                column_names = ['output']

        if result == [{'output': 'Queries matched'}]:
            self.data = 0
            metricdic = {'Queries not matched': self.data}
            return ValidationResult(ValidationResult.PASS, result, column_names, metricdic)
        else:
            self.data = 1
            metricdic = {'Queries not matched': self.data}
            return ValidationResult(ValidationResult.FAIL, result, column_names, metricdic)

    @staticmethod
    def required_parameters():
        return [('connection1',  [SQLAlchemyConnection, JDBCConnection]), ('connection2',  [SQLAlchemyConnection, JDBCConnection]), ('query1', str), ('query1_key', str), ('query2', str), ('query2_key', str), ('pass_condition', str)]

    @staticmethod
    def optional_parameters():
        return [('tolerance_percentage', str), ('field_name', str)]

    @staticmethod
    def ui_fields():
        connection_field_1 = ConnectionField(parameter_name='connection1', label='Connection 1',
                                             description='Choose the connection of the first query for comparison', default_value=None, type_filter=['SQLAlchemy', 'JDBC'], name_filter=None)
        query_1 = TextAreaField(parameter_name='query1', label='Query 1',
                                description='Enter the SQL query to run on Connection 1', placeholder='Please limit the number of results returned in your sql query and do not use select * .')
        query_1_key = TextField(parameter_name='query1_key', label='Query 1 Key',
                                description='Enter the key column from the results of Query 1 to join to on the results from Query 2')
        connection_field_2 = ConnectionField(parameter_name='connection2', label='Connection 2',
                                             description='Choose the connection of the second query for comparison', default_value=None, type_filter=['SQLAlchemy', 'JDBC'], name_filter=None)
        query_2 = TextAreaField(parameter_name='query2', label='Query 2',
                                description='Enter the SQL query to run on Connection 2', placeholder='Please limit the number of results returned in your sql query and do not use select * .')
        query_2_key = TextField(parameter_name='query2_key', label='Query 2 Key',
                                description='Enter the key column from the results of Query 2 to join to on the results from Query 1')
        pass_condition = SelectField(parameter_name='pass_condition', label='Pass Condition', description='Choose the pass condition', selection_list=[(
            'Query 1 and Query 2 data is the same for all rows that join in both queries', 'Query 1 and Query 2 data is the same for all rows that join in both queries'), ('Query 1 and Query 2 data is exactly the same', 'Query 1 and Query 2 data is exactly the same')])
        field_name = TextAreaField(parameter_name='field_name', label='Field names', rows=1,
                                   description='Enter the list of Field names', placeholder='Please, add a comma separated list of field names.')
        tolerance_percentage = TextAreaField(parameter_name='tolerance_percentage', label='Tolerance percentages', rows=1,
                                             description='Enter the list of tolerance percentage for field names', placeholder='Please, add a comma separated list of numeric tolerance for numeric field names.')
        return[connection_field_1, query_1, query_1_key, connection_field_2, query_2, query_2_key, pass_condition, field_name, tolerance_percentage]

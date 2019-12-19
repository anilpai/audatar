import great_expectations as ge
from types import FunctionType

from inspect import signature
import pprint

from audatar.validators import ValidatorBase
from audatar.connections import SQLAlchemyConnection
from audatar.ui import ConnectionField, TextAreaField
import pandas as pd
import great_expectations.dataset as dataset
from sqlalchemy import create_engine
from great_expectations import util


class GreatExpectationsValidator(ValidatorBase):
    """A validator that validates expectations defined by Great Expectations library.
    """
    def __init__(self, input_parameters):
        super().__init__(input_parameters)
        parameters = self.parameter_values()

        self.connection = parameters['connection_string']

    def validate(self):

        con = create_engine(self.connection)

        query = "<enter_query>"
        try:
            df = pd.read_sql(query, con)
            df = util._convert_to_dataset_class(df, dataset.pandas_dataset.PandasDataset)
            return df

        except Exception as e:
            return str(e)

    @staticmethod
    def required_parameters():
        return [('connection', [SQLAlchemyConnection]), ('query', str)]

    @staticmethod
    def ui_fields():
        connection_field = ConnectionField(parameter_name='connection', label='Connection',
                                           description='Choose a connection', type_filter=['SQLAlchemy'],
                                           name_filter=None, default_value=None)
        query_field = TextAreaField(parameter_name='query', label='Query', description='Enter a valid SQL query',
                                    rows=20, default_value=None, placeholder='Please limit the number of results returned in your sql query and do not use select * .')
        return [connection_field, query_field]



connection_string = "<enter_connecting_string>"
validator = GreatExpectationsValidator({'connection_string': connection_string})
result = validator.validate()

print("Result")
print("======")
print("GE Dataframe Result:\n {}".format(result))
print("result type: {}".format(type(result)))

print("### Great Expectations ###")
print("###\n expect_column_to_exist \n###")
columns = ['id_result', 'SiteId', 'SiteName', 'WebsiteUrl']
for col_name in columns:
    print(result.expect_column_to_exist(col_name))

print(result.expect_table_columns_to_match_ordered_list(columns))

values = {"column": "id_result", "min_value": 0, "max_value": 165}
print(result.expect_column_values_to_be_between(**values))


def get_all_expectations():
    o = ge.dataset.base.Dataset
    return {x: [s.split('=')[0].lstrip() for s in str(signature(getattr(o, x))).split(',')[1:]] for x, y in
            o.__dict__.items() if type(y) == FunctionType and x.startswith('expect_')}


pprint.pprint(get_all_expectations())


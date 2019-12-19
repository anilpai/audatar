import decimal
import json
from collections import OrderedDict
import dateutil.parser

from audatar.utils.jsonhelper import encode_base


class ValidationResult:
    PASS = 'Pass'
    FAIL = 'Fail'

    def __init__(self, status, results=None, column_order=None, metricdic = None):
        # Validate status is either 'Pass' or 'Fail'
        if not (status == ValidationResult.PASS or status == ValidationResult.FAIL):
            raise ValueError('Validation status should be either Pass or Fail.')
        self.status = status
        self.column_order = column_order
        self.columns = None

        # Validate results is a list of dictionaries where each dictionary contains the same keys and value types.
        if results is not None:
            if not isinstance(results, list):
                raise TypeError('Validation results should be a list of dictionaries with the same key and value types.')
            elif len(results) > 0:
                for result in results:
                    if not isinstance(result, dict):
                        raise TypeError(
                            'Validation results should be a list of dictionaries with the same key and value types.')
                    else:
                        if self.columns is None:
                            self.columns = {key: type(value).__name__ for (key, value) in result.items()}
                        else:
                            if len(list(result.keys())) != len(list(self.columns.keys())):
                                raise ValueError(
                                    'All dictionaries in the validation result should contain the same number of key/value pairs.')
                            for key, value in result.items():
                                if key not in self.columns or self.columns[key] != type(value).__name__:
                                    raise ValueError(
                                        'All dictionaries in the validation result should contain the same keys and value types.')
                    # Validate column order
                    if column_order is None:
                        self.column_order = list(self.columns.keys())
                    else:
                        for column in self.column_order:
                            if column not in self.columns:
                                raise ValueError(
                                    'Column order list should contain only column names that match the validation result records.')
            else:
                return ValueError('Validation result list should not be empty.')
        self.results = results
        self.metricdic = metricdic

    def result_records_json(self):
        if self.results is None:
            return ''
        else:
            jsondict = OrderedDict([('schema', OrderedDict([('columns', self.columns),
                                                            ('colOrder', self.column_order)])),
                                    ('data', self.results)])
            jsonobj = json.dumps(jsondict, indent=4, default=encode_base)
            return jsonobj
    def metric_json(self):
        if self.results is None:
            return ''
        else:
            
            json_string = json.dumps(self.metricdic, indent=4, default=encode_base)
            return json_string

    @staticmethod
    def json_result_records_to_dict(jsonResultRecords):
        jsonDict = json.loads(jsonResultRecords)
        columns = jsonDict['schema']['columns']
        results = jsonDict['data']
        for result in results:
            for key, value in result.items():
                if columns[key] == 'Decimal':
                    result[key] = decimal.Decimal(value)
                elif columns[key] == 'datetime':
                    result[key] = dateutil.parser.parse(value)
        return results

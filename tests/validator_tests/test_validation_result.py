import pytest
import decimal
import datetime
import json

from audatar.validators.validationresult import ValidationResult


class TestValidationResult:

    given_1 = [{'a': decimal.Decimal(1), 'b': 'test',
                'c': datetime.datetime.now()},
               {'a': decimal.Decimal(2), 'b': 'test2',
                'c': datetime.datetime.now()}]

    expected_1 = given_1

    test_data = [
        (given_1, expected_1)
    ]

    @pytest.mark.parametrize('given,expected', test_data)
    def test_validation_result(self, given, expected):
        actual = ValidationResult(ValidationResult.PASS, results=given)
        assert actual.status == 'Pass'
        assert json.loads(actual.result_records_json())['data'][0]['a'] == given[0]['a']
        assert json.loads(actual.result_records_json())['data'][0]['b'] == given[0]['b']
        assert json.loads(actual.result_records_json())['data'][1]['a'] == given[1]['a']
        assert json.loads(actual.result_records_json())['data'][1]['b'] == given[1]['b']

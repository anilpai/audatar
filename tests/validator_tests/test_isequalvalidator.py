import pytest


@pytest.mark.unit
def test_one():
    assert True


@pytest.mark.unit
def test_two():
    assert True

#
#
# from validators import IsEqualValidator
#
#
# # Create input parameters for validator
#
# input_parameters = {'d':1,'a':1,'c':1,'b':1}
# print("input: {}".format(input_parameters))
#
# # Create instance of IsEqualValidator
#
# validator = IsEqualValidator(input_parameters)
#
# # Validate the values in input are all equal and store result
#
# result = validator.validate()
#
# print("Result")
# print("======")
# print("Status: {}".format(result.status))
# print("Results JSON:")
# print(result.result_records_json())

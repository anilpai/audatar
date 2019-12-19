import pytest
from audatar.utils import helper


class TestHelper:

    testdata = [
        (20, 'PR_VLD_ConnectTrips'),
        (30, 'PR_VLD_BrandInvPayDifference'),
        (44, 'PR_VLD_ListingsWithMultipleActiveSubscriptions')
    ]

    @pytest.mark.parametrize('given,expected', testdata)
    def test_get_vc_by_id(self, app, given, expected):
        assert helper.get_vc_by_id(given).name == expected

    @pytest.mark.parametrize('expected,given', testdata)
    def test_get_vc_by_name(self, app, given, expected):
        assert helper.get_vc_by_name(given).id == expected

    test_validator = [
        (1, 'LegacyEDWValidator'),
        (2, 'SqlDataValidator'),
        (3, 'S3FolderValidator'),
        (4, 'RecordCountComparisonValidator')
    ]

    @pytest.mark.parametrize('given,expected', test_validator)
    def test_get_validator_class_path_by_id(self, app, given, expected):
        assert helper.get_validator_class_path_by_id(
            given) == 'audatar.validators.{0}.{1}'.format(expected.lower(), expected)

    test_connection = [
        (3, 'AWS_connect'),
        (4, 'EDW MSSQL DEV'),
        (5, 'Hive ON-PREM DEV')
    ]

    @pytest.mark.parametrize('expected,given', test_connection)
    def test_get_conn_by_name(self, app, given, expected):
        assert helper.get_conn_by_name(given).id == expected

    test_connection_type = [
        (101, 'SQLAlchemy'),
        (102, 'AWS')
    ]

    @pytest.mark.parametrize('given, expected', test_connection_type)
    def test_get_conn_type_by_id(self, app, given, expected):
        assert helper.get_conn_type_by_id(given).id == given
        assert helper.get_conn_type_by_id(given).name == expected

    test_class_path = [
        ('SQLAlchemyConnection'),
        ('AWSConnection')
    ]

    @pytest.mark.parametrize('given', test_class_path)
    def test_get_class_by_class_path(self, app, given):
        import inspect
        class_name = 'audatar.connections.{0}.{1}'.format(given.lower(), given)
        assert inspect.isclass(helper.get_class_by_class_path(class_name))

    test_validation_check_parameters = [
        (12, 1444, 1949),
        (13, 1445, 1950)
    ]

    @pytest.mark.parametrize('given,expected1,expected2', test_validation_check_parameters)
    def test_get_vcp_by_id(self, app, given, expected1, expected2):
        assert len(helper.get_vcp_by_id(given)) == 2
        assert helper.get_vcp_by_id(given)[0].id == expected1
        assert helper.get_vcp_by_id(given)[1].id == expected2

    test_conn_params = [
        ('Hive ON-PREM DEV', ['connection_args', 'connection_string']),
        ('EDW MSSQL DEV', ['connection_string']),
        ('AWS_connect', ['aws_access_key_id', 'aws_secret_access_key', 'region', 'service'])
    ]

    @pytest.mark.parametrize('given,expected', test_conn_params)
    def test_get_connection_parameters(self, app, given, expected):
        for item in helper.get_connection_parameters(given):
            if isinstance(item, dict):
                assert sorted(list(item.keys())) == sorted(expected)

    test_connection_names = [
        ('AWS_connect'),
        ('EDW MSSQL DEV'),
        ('Hive ON-PREM DEV')
    ]

    @pytest.mark.parametrize('given', test_connection_names)
    def test_get_conn_class_by_conn_name(self, app, given):
        import inspect
        assert inspect.isclass(helper.get_conn_class_by_conn_name(given))

    test_times = [
        (1505221440, '2017-09-12 08:04:00'),
        (576116820, '1988-04-03 19:27:00')
    ]

    @pytest.mark.parametrize('given,expected', test_times)
    def test_format_time(self, app, given, expected):
        assert helper.format_time(given) == expected

    test_colors = [
        ('Started', 'YELLOW'),
        ('Submitted', 'YELLOW'),
        ('Fail', 'RED'),
        ('Success', 'GREEN')
    ]

    @pytest.mark.parametrize('given,expected', test_colors)
    def test_convert_to_dr_color(self, app, given, expected):
        assert helper.convert_to_dr_color(given) == expected

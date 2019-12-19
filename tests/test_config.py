import pytest
from audatar import audatar_config
import os


class TestConfig:

    test_validation_check_parameters = [
        ('ae-audatar', 'test', '1.2345', 'us-aus-1-dts', 'http://ae-audatar-test.us-aus-1-dts.slb.dts.vxe.away.black'),
        ('foo', 'stage', '1.23', 'us-east-1-vpc-35196a52', 'http://foo-stage.us-east-1-vpc-35196a52.slb.dts.vxe.away.black')
    ]

    @pytest.mark.skip
    @pytest.mark.parametrize('given1,given2,given3,given4,expected', test_validation_check_parameters)
    def test_get_vcp_by_id(self, given1, given2, given3, given4, expected):
        os.environ.setdefault('MPAAS_APPLICATION_NAME', given1)
        os.environ.setdefault('MPAAS_ENVIRONMENT', given2)
        os.environ.setdefault('MPAAS_APPLICATION_VERSION', given3)
        os.environ.setdefault('MPAAS_REGION', given4)
        assert audatar_config.generate_mpaas_url() == expected

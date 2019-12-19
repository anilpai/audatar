"""to test a Validation Check input: vc_name or vc_id and optional parameters
output: vc_status as "pending" or "success" or "failure"."""

import pytest
import requests
import json
import time
from requests.auth import HTTPBasicAuth
from audatar import audatar_config
from audatar.utils import helper


class RunVC:

    test_connection = [
        ('dev_aws'),
        ('stage_aws'),
        ('prod_aws')
    ]

    @pytest.mark.xskip
    def test_run_vc_for_s3_folder_validator(self, test_client):
        """S3 Folder validator."""
        optional_params = {'connection': 'dev_aws', 'bucket': 'vpopale'}
        parameters = {'validation_check_id': 23, 'opts_params': optional_params}
        r = test_client.get('/api/runVC', data=json.dumps(parameters, indent=4))
        assert r.status_code == 200
        assert json.loads(r.data.decode())['status'] in ['Started', 'Pending']

        # resp = test_client.get('/api/vc/id/11')
        # assert resp.status_code == 200
        # data = json.loads(resp.data.decode())
        # assert list(data.keys()) == ['dataset_id','description','dimension_id','documentation_url','id','input','is_active','name','severity_level_id','team_id','validator_id']
        # assert resp.status_code == 200

    @pytest.mark.xskip
    def test_run_vc_for_legacy_edw_validator(self, test_client):
        """Legacy EDW validator."""
        optional_params = {'connection': 'EDW_MSSQL'}
        parameters = {'validation_check_name': 'PR_VLD_SiteMissingGoogleAnalyticsAccount', 'opts_params': optional_params}
        assert False

    @pytest.mark.xskip
    def test_run_vc_for_hive_data_validator(self, test_client):
        """Hive Data validator."""

        optional_params = {'connection': 'HIVE_SQL'}
        parameters = {'validation_check_id': 259, 'opts_params': optional_params}
        assert False

    @pytest.mark.xskip
    def test_run_vc_for_sql_data_validator(self, test_client):
        """SQL Data validator."""

        optional_params = {'connection': 'EDW_MSSQL'}
        parameters = {'validation_check_name': 'PR_VLD_SiteMissingGoogleAnalyticsAccount', 'opts_params': optional_params}
        assert False

    test_vc_ids = [11, 12, 13]

    @pytest.mark.xskip
    @pytest.mark.parametrize(test_vc_ids)
    def test_run_on_dev(self, test_client, vc_ids):
        for i in vc_ids:
            optional_params = {}
            parameters = {'validation_check_id': 116, 'opts_params': optional_params}
            r = requests.post('{0}/api/runVC'.format(audatar_config.aws_env['aws_prod']), data=json.dumps(
                parameters, indent=4), verify=False, headers=audatar_config.headers)

            print(r)
            if r.status_code == 200:
                print(r.json())
            else:
                print(r.content)

    @pytest.mark.xskip
    def test_notification_log_create(self, test_client):

        parameters = {'task_id': '8587ef6f-8061-44c8-ad1b-50646b7016f9',
                      'validator_id': 1,
                      'time_completed': helper.format_time(time.time())
                      }

        r = requests.post('http://localhost:8080/api/nlog/create', data=json.dumps(parameters, indent=4),
                          verify=False, headers=audatar_config.headers)
        print(r)
        if r.status_code == 200:
            print(r.json())
        else:
            print(r.content)

    @pytest.mark.xskip
    def test_notification_log_delete(self, test_client):

        r = requests.delete('http://localhost:8080/api/nlog/delete/1', verify=False,
                            headers=audatar_config.headers)
        print(r)
        if r.status_code == 200:
            print(r.json())
        else:
            print(r.content)

    @pytest.mark.xskip
    def test_validation_check_create(self, test_client):

        parameters = {'name': 'test_name',
                      'is_active': False,
                      'validator_id': 1,
                      'description': 'test description',
                      'team_id': 9,
                      'dataset_id': 4,
                      'severity_level_id': 2
                      }

        r = requests.post('http://localhost:8080/api/vc/create',
                          headers=audatar_config.headers, data=json.dumps(parameters, indent=4))
        print(r)
        if r.status_code == 200:
            print(r.json())
        else:
            print(r.content)

    @pytest.mark.xskip
    def test_validation_check_delete(self, test_client):
        r = requests.delete('http://localhost:8080/api/vc/delete/263', headers=audatar_config.headers)
        print(r)
        if r.status_code == 200:
            print(r.json())
        else:
            print(r.content)

    @pytest.mark.xskip
    def test_connection_create(self, test_client):

        parameters = {'connection_type_id': 1,
                      'description': 'test description',
                      'name': 'test_name'
                      }

        r = requests.post('http://localhost:8080/api/connection/create',
                          headers=audatar_config.headers, data=json.dumps(parameters, indent=4))

        print(r)
        if r.status_code == 200:
            print(r.json())
        else:
            print(r.content)

    @pytest.mark.xskip
    def test_connection_delete(self, test_client):

        r = requests.delete('http://localhost:8080/api/connection/delete/4', headers=audatar_config.headers)

        print(r)
        if r.status_code == 200:
            print(r.json())
        else:
            print(r.content)

    @pytest.mark.xskip
    def filterable_api(self, test_client):

        parameters = {'dataset_id': 4}

        r = requests.get('http://localhost:8080/api/vc', params=parameters,
                         headers=audatar_config.headers)

        print(r.json())

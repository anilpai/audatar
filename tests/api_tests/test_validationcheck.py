import json
import pytest


class TestAPIValidationCheck:

    test_validation_checks = [
        (11, 'PR_VLD_BrandZombieDetect'),
        (116, 'PR_VLD_3PD_revshare_no_DistributionId'),
        (258, 'PR_VLD_BQF_visitorFact_End_completion')
    ]

    @pytest.mark.parametrize('given,expected', test_validation_checks)
    def test_get_vc_by_id(self, test_client, given, expected):
        resp = test_client.get('/api/vc/id/{0}'.format(given))
        data = json.loads(resp.data.decode())
        assert resp.status_code == 200
        assert sorted(data.keys()) == sorted(['dataset_id', 'description', 'dimension_id', 'documentation_url', 'id', 'input',
                                              'is_active', 'name', 'severity_level_id', 'team_id', 'validator_id'])
        assert data['name'] == expected

    @pytest.mark.parametrize('expected,given', test_validation_checks)
    def test_get_vc_by_name(self, test_client, given, expected):
        resp = test_client.get('/api/vc/name/{0}'.format(given))
        data = json.loads(resp.data.decode())
        assert resp.status_code == 200
        assert sorted(data[0].keys()) == ['dataset_id', 'description', 'dimension_id', 'documentation_url', 'id', 'input',
                                          'is_active', 'name', 'severity_level_id', 'team_id', 'validator_id']
        assert data[0]['id'] == expected

    def test_list_of_validation_checks(self, test_client):
        resp = test_client.get('/api/vc/')
        assert resp.status_code == 200
        data = json.loads(resp.data.decode())
        assert data['count'] > 250

    @pytest.mark.xskip
    def test_create_vc(self, test_client):
        parameters = {'name': 'test_name',
                      'is_active': False,
                      'validator_id': 1,
                      'description': 'test description',
                      'team_id': 9,
                      'dataset_id': 4,
                      'severity_level_id': 2
                      }

        resp = test_client.post('/api/vc/create', data=json.dumps(parameters, indent=4))
        assert resp.status_code == 401

    @pytest.mark.xskip
    def test_delete_vc(self, test_client):
        assert True

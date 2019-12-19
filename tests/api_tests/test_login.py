import json
import pytest


class TestAPILogin:

    credentials = [
        ('ha_username', 'ha_password')
    ]

    @pytest.mark.parametrize('username,password', credentials)
    @pytest.mark.xskip
    def test_login_for_a_user(self, test_client, username, password):

        credentials = {	'username': username, 'password': password}
        r = test_client.post('http://localhost:8080/api/login',
                             data=json.dumps(credentials),
                             headers={'accept': 'application/json', 'content-type': 'application/json'}
                             )
        data = json.loads(r.data.decode())

        assert r.status_code == 200
        assert data['token'] is not None

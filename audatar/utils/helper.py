import logging
import importlib
import json
import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import jwt
from audatar import audatar_config
from audatar.models import Connection, ConnectionParameter, ConnectionType
from audatar.models import ValidationCheck, ValidationCheckInstance, ValidationCheckParameters, Validator
from audatar.utils import Crypto
from audatar.utils.jsonhelper import encode_base
from flask import request
from dateutil import tz


def get_vc_by_id(id):
    """get Validation Check using VC ID."""
    vc = ValidationCheck.query.get(id)
    return vc


def get_vc_by_name(name):
    """get Validation Check using VC Name."""
    vc = ValidationCheck.query.filter(ValidationCheck.name == name).one_or_none()
    return vc


def get_validator_class_path_by_id(id):
    """get validator Class Path using id.

    :param id: validator id.
    :return: classpath corresponding to validator id.
    """
    validator = Validator.query.get(id)
    return validator.class_path


def get_conn_by_name(name):
    """get connection details using connection name.

    :param name: connection name
    :return: connection object
    """
    conn = Connection.query.filter(Connection.name == name).one_or_none()
    return conn


def get_conn_type_by_id(id):
    """get connection Type using id.

    :param id: connection id.
    :return: connection type object.
    """
    conn_type = ConnectionType.query.get(id)
    return conn_type


def get_class_by_class_path(class_path):
    """get connection class using class_path."""
    class_path = class_path.rsplit('.', 1)
    module = class_path[0]
    class_name = class_path[1]
    return getattr(importlib.import_module(module), class_name)


def get_vcp_by_id(id):
    """gets Validation Check Parameters by.

    :param id: validation check id.
    :return: validation check parameter object.
    """
    return ValidationCheckParameters.query.filter(ValidationCheckParameters.validation_check_id == id).all()


def get_secret():
    """gets the secret key from Vault Server.

    :return: a secret key to use for decryption.
    """
    secret = audatar_config.secret_key
    return secret


def decrypt_conn_string(conn_string):
    c = Crypto(get_secret())
    return c.decode_text(conn_string)


def encrypt_conn_string(conn_string):
    c = Crypto(get_secret())
    return c.encode_text(conn_string)


def get_connection_parameters(connection_name):
    """get connection parameters.

    :param connection_name: name of the connection.
    :return: a dictionary of connection parameters.
    """

    logging.info('Get connection id')
    conn_id = get_conn_by_name(connection_name).id

    logging.info('Get connection class')
    conn_class = get_conn_class_by_conn_name(connection_name)

    logging.info('get valid connection parameters')

    valid_conn_params = conn_class.required_parameters() + conn_class.optional_parameters()
    valid_conn_params_dict = {}
    for k, v in valid_conn_params:
        valid_conn_params_dict[k] = v

    conn_params = [{'parameter_name': c.parameter_name, 'parameter_value': c.parameter_value}
                   for c in ConnectionParameter.query.filter(ConnectionParameter.connection_id == conn_id).all()]

    logging.info('building connection parameters dictionary')

    conn_params_dict = {}
    for conn_param in conn_params:
        if isinstance(valid_conn_params_dict[conn_param['parameter_name']], dict):
            conn_params_dict[conn_param['parameter_name']] = decrypt_conn_string(
                json.loads(conn_param['parameter_value']))
        else:
            conn_params_dict[conn_param['parameter_name']] = decrypt_conn_string(conn_param['parameter_value'])

    logging.info('connection parameters dictionary built !')

    conn = get_conn_by_name(connection_name)
    conn_type = get_conn_type_by_id(conn.connection_type_id)

    return conn_params_dict, conn_type.class_path


def get_conn_class_by_conn_name(conn_name):
    """Get Connection Class using a Connection Name.

    :param conn_name: name of the connection.
    :return: connection class
    """
    conn = get_conn_by_name(conn_name)
    conn_type = get_conn_type_by_id(conn.connection_type_id)
    conn_class = get_class_by_class_path(conn_type.class_path)
    return conn_class


def create_vci_entry(vc, result, params_for_validator, user):
    """Creates a new record on Validation Check Instance table.

    :param vc: validation check
    :param result: celery task result
    :param params_for_validator: parameters passed to celery task.
    :return: id of new vci instance.
    """

    parameters = {'task_id': result.task_id,
                  'validation_check_id': vc['id'],
                  'input': json.dumps(params_for_validator, indent=4, default=encode_base),
                  'time_submitted': format_time(time.time()),
                  'status': 'Submitted',
                  'created_by': user
                  }

    new_task = requests.post('{0}/vci/'.format(audatar_config.api_url), headers=generate_headers(
        request.headers.get('Authorization').split()[1]), data=json.dumps(parameters, indent=4)).json()
    return new_task['id']


def get_celery_task_times(task_id):
    """Gets Celery task times (time_started, time_completed etc).

    :param task_id: id of the celery task.
    :return: dictionary of task_times.
    """
    task_times = requests.get('{0}/api/task/info/{1}'.format(audatar_config.flower_api_url, task_id),
                              auth=(audatar_config.flower_username, audatar_config.flower_password)).json()
    return task_times


def format_time(timestamp):
    """Converts a unix timestamp to date & time in local time.

    :param timestamp: unix timestamp.
    :return: formatted date-time string.
    """
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))


def get_user(token):
    """Decodes a jwt_token and gets the username.

    :param token: JSON Web Token.
    :return: username of the user.
    """
    data = jwt.decode(
        token,
        audatar_config.secret_key,
        options=dict(verify_exp=False)
    )
    return data['username']


def get_is_admin(token):
    """Decodes a jwt_token and gets the role.

    :param token: JSON Web Token.
    :return: role of the user.
    """
    data = jwt.decode(
        token,
        audatar_config.secret_key,
        options=dict(verify_exp=False)
    )
    return data['isAdmin']


def get_expiration(token):
    """Decodes a jwt_token and gets the expiration.

    :param token: JSON Web Token.
    :return: expiration from token.
    """
    data = jwt.decode(
        token,
        audatar_config.secret_key,
        options=dict(verify_exp=False)
    )
    return data['exp']


def generate_headers(token):
    """Generates Headers using a token.

    :param token: JWT
    :return: headers
    """
    return {'accept': 'application/json', 'Authorization': 'Bearer '+token}


def generate_logging_message(user, object_name, method, id, status, message):
    """Genarates logging message with a delimiter."""
    message = '{0} | {1} | {2} | {3} | {4} | {5}'.format(str(user), str(object_name), str(method), str(id), str(status),
                                                         str(message))
    return message


def convert_time_to_cst(utc_time):
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('US/Central')
    utc_time = utc_time.replace(tzinfo=from_zone)
    cst_time = utc_time.astimezone(to_zone)

    return cst_time


def requests_retry_session(
    retries=5,
    back_off_factor=0.2,
    status_force_list=(500, 502, 503, 504),
    session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=back_off_factor,
        status_forcelist=status_force_list,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def get_results_dict(vci_id):
    vci_result = ValidationCheckInstance.query.get(vci_id)
    vc_result = ValidationCheck.query.get(vci_result.validation_check.id)
    vci_result_url = audatar_config.audatar_vci_url + str(vci_id)
    vci_result_metric = json.loads(vci_result.result_metric)
    tags = []
    if vc_result.tags is not None:
        tags = [t.strip() for t in vc_result.tags.split(',')]
    ''' Add standard tags.'''
    tags.append('audatar')
    tags.append(audatar_config.env)
    result_dict = {
                'dataSetUuid': vc_result.dataset_id,
                'healthCheckName': vc_result.name,
                'lastRunStatus': convert_to_dr_color(vci_result.result),
                'description': vc_result.description,
                'externalLinks': {
                        'Validation check instance details': vci_result_url
                },
                'lastRun': vci_result.time_completed.strftime("%s"),
                'tags': tags,
                'owner': vci_result.created_by,
                'portfolioId': vc_result.team_id,
                'details': vc_result.documentation_url,
                'statistics': vci_result_metric
                }

    return result_dict


def convert_to_dr_color(run_status):
    if run_status in ['Fail', 'Error']:
        return 'RED'
    elif run_status in ['Pass']:
        return 'GREEN'
    else:
        return 'YELLOW'


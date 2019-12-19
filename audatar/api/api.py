import json
import logging
import ldap3
import jwt
import datetime
from audatar import audatar_config
from functools import wraps

from flask import Blueprint, jsonify, request, abort, g

from audatar import task_executor
from audatar.models import User, Jwtblacklist, Validgroups
from audatar.utils import helper
from audatar.extensions import db, auth

from flask_cors import CORS
from flasgger import swag_from

""" The api stuff """

api_bp = Blueprint('api_bp', __name__, url_prefix='/api')

CORS(api_bp)
logger = logging.getLogger('audatar')


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        token = request.headers.get('Authorization', None)

        if token is None:
            return jsonify({'message': 'Token is missing in headers'}), 401

        parts = token.split()

        if parts[0].lower() != 'Bearer'.lower():
            msg = 'Unsupported authorization type'
            return jsonify({'message': msg}), 400
        elif len(parts) == 1:
            msg = 'Token missing'
            return jsonify({'message': msg}), 400
        elif len(parts) > 2:
            msg = 'Token contains spaces'
            return jsonify({'message': msg}), 400

        try:
            data = jwt.decode(
                parts[1],
                audatar_config.secret_key,
                options=dict(verify_exp=False)
            )
            user = data['username']

            if user is None:
                return jsonify({'message': 'User doesnt exist'}), 401

        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid'}), 400

        return f(*args, **kwargs)
    return decorated


@api_bp.route('/login', methods=['POST'])
@swag_from('yml/login.yml')
def login():

    parameters = json.loads(request.data.decode('utf-8'))
    username = parameters.get('username')
    password = parameters.get('password')

    ha_username = 'wvrgroup\\{0}'.format(username)
    ha_password = password

    ''' Send request to AD '''
    try:
        server = ldap3.Server(audatar_config.LDAP_URI, get_info=ldap3.ALL)
        conn = ldap3.Connection(server, ha_username, ha_password, True)
        logger.info(helper.generate_logging_message(username, 'login api', 'POST', username,
                                                    'success', 'Success login in AD {}'.format(conn.extend.standard.who_am_i())))
    except ldap3.core.exceptions.LDAPBindError as bind_error:
        logger.info(helper.generate_logging_message(username, 'login api', 'POST', username, 'fail', str(bind_error)))
        return jsonify(flag='fail', msg=str(bind_error)), 401
    except ldap3.core.exceptions.LDAPPasswordIsMandatoryError as pwd_mandatory_error:
        logger.info(helper.generate_logging_message(username, 'login api',
                                                    'POST', username, 'fail', str(pwd_mandatory_error)))
        return jsonify(flag='fail', msg=str(pwd_mandatory_error)), 401

    '''Filter for username'''

    ad_filter = '(&(sAMAccountType=805306368)(sAMAccountName=' + username + '))'
    conn.search('dc=wvrgroup,dc=internal', ad_filter)
    person = conn.entries

    '''Get user's groups'''
    fq_persons = [result.entry_dn for result in person]
    my_groups = []
    for person in fq_persons:
        conn.search(person, '(objectclass=person)', attributes=['memberOf'])
        if 'memberOf' in conn.entries[0]:
            list_of_groups = conn.entries[0]['memberOf'].values
            for listgr in list_of_groups:
                conn.search(listgr, '(objectclass=group)', attributes=['cn'])
                if 'cn' in conn.entries[0]:
                    ind_groups = conn.entries[0]['cn'].values[0]
                    my_groups.append(ind_groups)

    '''Validate if user belongs to Audatar admin group'''
    isAdmin = True if 'audatar_admins' in my_groups else False

    '''Generate token'''

    try:
        exp = datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        token = jwt.encode({'username': username, 'exp': exp, 'isAdmin': isAdmin}, audatar_config.secret_key)
        logger.info(helper.generate_logging_message(username, 'login api', 'POST', username, 'success',
                                                'User has logged in successfully'))
        epoch = datetime.datetime.utcfromtimestamp(0)
        resp = jsonify(flag='pass', token=token.decode('ascii'), username=username, isAdmin=isAdmin,
                       exp=int((exp - epoch).total_seconds() * 1000))
        resp.status_code = 200
        resp.headers.extend({'jwt-token': token})
        return resp
    except Exception as e:
        logger.info(helper.generate_logging_message(username, 'login api', 'POST', username, 'fail', str(e)))
        return jsonify(flag='fail', msg='Sorry, something went wrong : {0} '.format(username)), 401


@api_bp.route('/tokentest')
@token_required
def get_tokentest():
    token = request.headers.get('Authorization')
    parts = token.split()
    user = helper.get_user(parts[1])
    exp = helper.get_expiration(parts[1])
    rol = helper.get_is_admin(parts[1])
    return jsonify({'message': 'Good, if you see this, your token is OK  user: {0} and Admin: {1} and exp: {2}'.format(user, rol, exp)})


@api_bp.route('/users', methods=['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        return jsonify('missing arguments'), 400
    if User.query.filter_by(username=username).first() is not None:
        return jsonify('existing user'), 400
    user = User(username=username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'username': user.username}), 201


@api_bp.route('/users/<int:id>')
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(400)
    return jsonify({'username': user.username})


@api_bp.route('/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(600)
    return jsonify({'token': token.decode('ascii'), 'duration': 600})


@api_bp.route('/logout', methods=['POST'])
@token_required
@swag_from('yml/logout.yml')
def logout():
    return jsonify(flag='success', msg='Logged out')


@api_bp.route('/getConnectionParameters/<conn_name>', methods=['GET'])
@token_required
def get_conn_params(conn_name):
    token = request.headers.get('Authorization')
    parts = token.split()
    user = helper.get_user(parts[1])
    if user != 'audatar':
        admin = helper.get_is_admin(parts[1])
        logger.warning(helper.generate_logging_message(user, 'getConnectionParameters api', 'GET', conn_name, 'success',
                                                       'User is getting Connection parameter details'))
        if not admin:
            return jsonify(flag='Fail', message='Option not available for non-admin users')
    result = helper.get_connection_parameters(conn_name)
    conn_params_dict = result[0]
    conn_class_path = result[1]
    return jsonify(flag='Success', conn_class_path=conn_class_path, parameters=conn_params_dict)


@api_bp.route('/runVC', methods=['POST'])
@token_required
@swag_from('yml/runVC.yml')
def run_validation():
    """takes vc_id or vc_name , and a dictionary of optional parameters.

    :return: json output
    """
    token = request.headers.get('Authorization')
    parts = token.split()
    user = helper.get_user(parts[1])

    parameters = json.loads(request.data.decode('utf-8'))
    logging.info(parameters)
    if 'validation_check_id' in parameters:
        validation_check = helper.get_vc_by_id(parameters['validation_check_id'])
        logging.info('Validation Check Id provided')
    elif 'validation_check_name' in parameters:
        validation_check = helper.get_vc_by_name(parameters['validation_check_name'])
        logging.info('Validation Check Name provided')
    else:
        raise ValueError('Either validation_check_id or validation_check_name must be specified.')

    if validation_check is None:
        return jsonify(flag='Failure', message='Please provide a valid validation_check_id or validation_check_name'), 404

    logging.info('Building validation check dictionary')
    vc = {'id': validation_check.id, 'name': validation_check.name, 'validator_id': validation_check.validator.id}
    logging.info('Validation check dictionary built !')

    vc_class_path = helper.get_validator_class_path_by_id(vc['validator_id'])
    logging.info('Got VC class path')

    validation_check_params_dict = {}

    logging.info('List of dictionaries from VC Parameters Table.')
    default_validation_check_params = [{'parameter_name': vcp.parameter_name,
                                        'parameter_value': vcp.parameter_value} for vcp in helper.get_vcp_by_id(vc['id'])]
    logging.info('default vc params built !')

    for param in default_validation_check_params:
        if param['parameter_name'] not in validation_check_params_dict:
            validation_check_params_dict[param['parameter_name']] = param['parameter_value']

    logging.info('Override the default parameters')

    for key, value in parameters['opts_params'].items():
        validation_check_params_dict[key] = value

    logging.info('validation_check_params_dict')
    logging.info(validation_check_params_dict)

    try:
        logging.info('Submitting the task to RabbitMQ')
        result = task_executor.validate.delay(vc_class_path, validation_check_params_dict)
        logging.info('Task %s is successfully submitted !', result.id)

        if result.id:
            logging.info('Update the Validation Check Instance table.')
            vci_id = helper.create_vci_entry(vc, result, validation_check_params_dict, user)
            logging.info('VCI Table updated successfully !')
            logger.warning(helper.generate_logging_message(user,
                                                           'runVC api', 'POST',
                                                           validation_check.id, 'success',
                                                           'User has executed VC: {0}, VCI: {1}'.format(validation_check.name, vci_id)))
        else:
            return jsonify(flag='Failure', msg='result object has no id'), 500
    except Exception as e:
        return jsonify(flag='Failure', msg='Task submission failed', exception=e), 500

    return jsonify(flag='Success', vci_id=vci_id, task_id=result.id, task_status=result.status), 200

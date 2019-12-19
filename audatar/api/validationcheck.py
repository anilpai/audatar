from flask import Blueprint, jsonify, request
import json
import time
import logging
import requests
from audatar.models import ValidationCheck, Validator, ValidationCheckParameters, Notification, Keyword
from audatar.serializers import vc_schema, vcs_schema
from audatar.extensions import db
from audatar.api import token_required
from flask_cors import CORS
from collections import Counter
from audatar.utils import helper
from audatar.utils.helper import get_class_by_class_path, format_time
from flasgger import swag_from
from audatar import audatar_config

validation_check_bp = Blueprint(
    'validation_check_bp', __name__, url_prefix='/api/vc')

CORS(validation_check_bp)
logger = logging.getLogger('audatar')


@validation_check_bp.route('/', methods=['GET'])
@token_required
@swag_from('yml/validationcheck_list.yml')
def list_of_validation_checks():
    """list all validation checks."""
    token = request.headers.get('Authorization')
    parts = token.split()
    user = helper.get_user(parts[1])

    parameters = request.args.to_dict(flat=True)

    ''' Filter conditions'''

    name_filter = parameters.get('name', None)

    """ Pagination parameters """
    pageSize = parameters.get('pageSize', None)
    pageNumber = parameters.get('pageNumber', None)

    """ Set defaults if not included in input, remove them so they are not included in filter"""
    if pageSize:
        parameters.pop('pageSize')
        pageSize = int(pageSize)
    else:
        pageSize = 10
    if pageNumber:
        parameters.pop('pageNumber')
        pageNumber = int(pageNumber)
    else:
        pageNumber = 1

    filter_queries = []
    order_queries = []

    """ Filter name using a case-insensitive LIKE instead of EQUALS """
    if name_filter:
        """Remove name parameter so that we don't include an equal filter
        too."""
        name_filter = '%{0}%'.format(name_filter)
        parameters.pop('name')
        filter_queries.append(ValidationCheck.name.ilike(name_filter))
        order_queries.append(ValidationCheck.name)

    vcs_all = ValidationCheck.query.filter_by(**parameters).filter(*filter_queries).order_by(*order_queries)

    """ Paginate query """
    vcs_all = vcs_all.paginate(per_page=pageSize, error_out=True)

    """ Return no data if result = 0 """
    if vcs_all.total == 0:
        return jsonify(count=0, data=[]), 200

    """ Go to pageNumber if it's valid """
    if pageNumber > vcs_all.pages:
        return jsonify(msg='error', summary='Bad Request', detail=' Invalid page number {}'.format(pageNumber)), 400
    else:
        vcs_all = vcs_all.query.paginate(
            page=pageNumber, per_page=pageSize, error_out=True)

    result = vcs_schema.dump(vcs_all.items)
    logger.info(helper.generate_logging_message(user, 'vc api', 'GET', 'list', 'success', 'Success Get vc list'))
    return jsonify(pageSize=pageSize, pageNumber=pageNumber, count=vcs_all.total, data=result.data), 200


@validation_check_bp.route('/<id>', methods=['GET'])
@token_required
@swag_from('yml/validationcheck_by_id.yml')
def get_vc_by_id(id):
    """detailed validation check by id."""
    token = request.headers.get('Authorization')
    parts = token.split()
    user = helper.get_user(parts[1])
    vc = ValidationCheck.query.get(id)
    if not vc:
        return jsonify({'Id': id,
                        'Message': 'Validation Check doesnt exist'}), 404
    logger.info(helper.generate_logging_message(user, 'vc api', 'GET', id, 'success', 'Success Get vc by ID'))
    return vc_schema.jsonify(vc), 200


@validation_check_bp.route('/<id>', methods=['DELETE'])
@token_required
@swag_from('yml/validationcheck_delete.yml')
def delete_vc(id):
    """delete validation check."""

    vc = ValidationCheck.query.get(id)
    vc_parameters = ValidationCheckParameters.query.filter(ValidationCheckParameters.validation_check_id == id)
    vc_keywords = Keyword.query.filter(Keyword.validation_check_id == id)
    vc_notifications = Notification.query.filter(Notification.validation_check_id == id)

    if vc is None:
        return jsonify({'Message': 'Validation Check Not Found'}), 404
    else:
        if vc_keywords:
            for keywords in vc_keywords:
                keywords.delete()

        if vc_parameters:
            for parameters in vc_parameters:
                parameters.delete()

        if vc_notifications:
            for notifications in vc_notifications:
                notifications.delete()

        vc.delete()

        return jsonify({'Message': 'Validation Check {0} successfully deleted'.format(vc.id)}), 200


@validation_check_bp.route('/', methods=['POST'])
@token_required
@swag_from('yml/validationcheck_post.yml')
def create_new_vc():
    """create new validation check."""
    token = request.headers.get('Authorization')
    parts = token.split()
    user = helper.get_user(parts[1])
    curr_time = format_time(time.time())

    # get parameters
    parameters = json.loads(request.data.decode('utf-8'))

    # get validator id
    validator_id = parameters.get('validator_id', None)

    # get tags
    vc_tags = parameters.get('tags', None)

    # get vc_params
    vc_parameters = parameters.get('parameters', None)

    # get class_path for validator

    validator = Validator.query.get(validator_id)
    validator_class = get_class_by_class_path(validator.class_path)
    required = validator_class.required_parameters()

    validator_list = []
    for name, typ in required:
        validator_list.append(name)

    vc_param_list = []
    for i in vc_parameters:
        if i['parameter_name'] in validator_list and i['parameter_value']:
            vc_param_list.append(i['parameter_name'])

    url = audatar_config.data_explorer_algolia_url
    payload = parameters.get('dataset_id', None)
    full_url = url + payload
    uuid_check = requests.get(full_url)
    if uuid_check.text == 'true':

        validation = (Counter(vc_param_list) == Counter(validator_list))

        if validation:

            try:

                # save validationCheck
                new_vc = ValidationCheck(name=parameters.get('name', None),
                                         is_active=parameters.get('is_active', None),
                                         validator_id=parameters.get('validator_id', None),
                                         description=parameters.get('description', None),
                                         team_id=parameters.get('team_id', None),
                                         dataset_id=parameters.get('dataset_id', None),
                                         dimension_id=parameters.get('dimension_id', None),
                                         severity_level_id=parameters.get('severity_level_id', None),
                                         documentation_url=parameters.get('documentation_url', None),
                                         time_updated=curr_time,
                                         updated_by=user,
                                         tags=vc_tags)

                new_vc.save()

                # get id from new validationcheck created
                id_vc = new_vc.id

                # save vc_params
                vc_parameters = parameters.get('parameters', None)
                for i in vc_parameters:
                    if i['parameter_value']:
                        new_vc_params = ValidationCheckParameters(validation_check_id=id_vc,
                                                                  parameter_name=i['parameter_name'],
                                                                  parameter_value=i['parameter_value'],
                                                                  time_updated=curr_time,
                                                                  updated_by=user)
                        new_vc_params.save()

                # save notifications
                vc_notifications = parameters.get('notifications', None)
                if vc_notifications:
                    for i in vc_notifications:
                        if i['type'] == '':
                            i['type'] = 'Email'
                        new_vc_notifications = Notification(validation_check_id=id_vc,
                                                            notify_if_failure=i['notify_if_failure'],
                                                            notify_if_success=i['notify_if_success'],
                                                            notify_if_error=i['notify_if_error'],
                                                            value=i['value'],
                                                            type=i['type'],
                                                            time_updated=curr_time,
                                                            updated_by=user)

                        new_vc_notifications.save()

                # save keywords
                vc_keywords = parameters.get('keywords', None)
                for i in vc_keywords:
                    new_vc_keywords = Keyword(validation_check_id=id_vc, keyword=i)
                    new_vc_keywords.save()

                # return response
                logger.info(
                    helper.generate_logging_message(user, 'vc api', 'POST', id_vc, 'success', 'Success create vc'))
                return vc_schema.jsonify(new_vc), 200

            except Exception as e:
                return jsonify({'Message': 'Error creating validation check: {}'.format(e)}), 400

        else:
            params_invalid = []
            for i in vc_param_list:
                if i not in validator_list:
                    params_invalid.append(i)
            return jsonify({'Message': 'Invalid parameters found', 'Parameters': params_invalid}), 404
    else:
        return jsonify({'Message': 'No record found in Data Explorer for the given data set uuid: {}'.format(payload)}), 400
        

@validation_check_bp.route('/<id>', methods=['PUT'])
@token_required
@swag_from('yml/validationcheck_put.yml')
def update_vc_by_id(id):
    token = request.headers.get('Authorization')
    parts = token.split()
    user = helper.get_user(parts[1])
    curr_time = format_time(time.time())

    """update validation check."""
    parameters = json.loads(request.data.decode('utf-8'))
    vc = ValidationCheck.query.get(id)

    if not vc:
        return jsonify({'Id': id,
                        'Message': 'Validation Check Instance was not created, hence cant be updated'}), 404

    # get validator id
    validator_id = parameters.get('validator_id', None)

    # get tags
    vc_tags = parameters.get('tags', None)

    # get vc_params
    vc_parameters = parameters.get('parameters', None)

    # get class_path for validator
    validator = Validator.query.get(validator_id)
    validator_class = get_class_by_class_path(validator.class_path)
    required = validator_class.required_parameters()

    # list required parameters
    validator_list = []
    for name, typ in required:
        validator_list.append(name)

    # list parameters from input, only required and not blank values
    vc_param_list = []
    for i in vc_parameters:
        if i['parameter_name'] in validator_list and i['parameter_value']:
            vc_param_list.append(i['parameter_name'])
    url = audatar_config.data_explorer_algolia_url
    payload = parameters.get('dataset_id', None)
    full_url = url + payload
    uuid_check = requests.get(full_url)
    if uuid_check.text == 'true':
        # compare required list and input list, true if input list has all required parameters
        validation = Counter(vc_param_list) == Counter(validator_list)

        if validation:
            
            # update vc payload
            vc.name = parameters.get('name', None)
            vc.is_active = parameters.get('is_active', None)
            vc.validator_id = parameters.get('validator_id', None)
            vc.description = parameters.get('description', None)
            vc.team_id = parameters.get('team_id', None)
            vc.dataset_id = parameters.get('dataset_id', None)
            vc.dimension_id = parameters.get('dimension_id', None)
            vc.severity_level_id = parameters.get('severity_level_id', None)
            vc.documentation_url = parameters.get('documentation_url', None)
            vc.time_updated = curr_time
            vc.updated_by = user
            vc.tags = vc_tags
            vc.save()

            # update parameters
            # list of new parameters (required and optional), not considering blank values
            param_new_list = []
            for i in vc_parameters:
                if i['parameter_value']:
                    param_new_list.append(i['parameter_name'])

            # list of original parameters
            validation_check_parameters = ValidationCheckParameters.query.filter(
                ValidationCheckParameters.validation_check_id == id)

            param_original_list = []
            for i in validation_check_parameters:
                param_original_list.append(i.parameter_name)

            # if no new parameters, then only update
            if Counter(param_new_list) == Counter(param_original_list):
                for j in vc_parameters:
                    vc_update = ValidationCheckParameters.query.filter(
                        ValidationCheckParameters.validation_check_id == id,
                        ValidationCheckParameters.parameter_name == j['parameter_name'])
                    for i in vc_update:
                        i.parameter_value = j['parameter_value']
                        i.time_updated = curr_time
                        i.updated_by = user
                        i.save()
                logger.info(helper.generate_logging_message(user, 'vc api', 'PUT',
                                                            id, 'success', 'Success vc parameters updated'))
            else:
                # delete optional parameters not sent in input
                for j in param_original_list:
                    if j not in param_new_list:
                        item_delete = ValidationCheckParameters.query.filter(
                            ValidationCheckParameters.validation_check_id == id,
                            ValidationCheckParameters.parameter_name == j)
                        logger.info(helper.generate_logging_message(user, 'vc api', 'PUT', id,
                                                                    'success',
                                                                    'Success vc update, deleted optional parameters'))
                        for i in item_delete:
                            db.session.delete(i)
                            db.session.commit()

                # get list of common parameters (input and original list)
                intersection = [i for i in param_new_list if i in param_original_list]

                if intersection:
                    for j in vc_parameters:
                        # update parameters in intersection
                        if j['parameter_name'] in intersection:
                            for i in intersection:
                                if j['parameter_name'] == i:
                                    vc_param_update = ValidationCheckParameters.query.filter(
                                        ValidationCheckParameters.validation_check_id == id,
                                        ValidationCheckParameters.parameter_name == i)

                                    for k in vc_param_update:
                                        k.parameter_value = j['parameter_value']
                                        k.time_updated = curr_time
                                        k.updated_by = user
                                        k.save()
                        else:
                            # insert new parameters not in intersection
                            if j['parameter_value']:
                                new_vc_params = ValidationCheckParameters(validation_check_id=id,
                                                                          parameter_name=j['parameter_name'],
                                                                          parameter_value=j['parameter_value'],
                                                                          time_updated=curr_time,
                                                                          updated_by=user)
                                new_vc_params.save()
                    logger.info(helper.generate_logging_message(user, 'vc api', 'PUT',
                                                                id, 'success', 'Success vc parameters updated'))
                else:
                    # insert new parameters (in case no intersection)
                    for j in vc_parameters:
                        new_vc_params = ValidationCheckParameters(validation_check_id=id,
                                                                  parameter_name=j['parameter_name'],
                                                                  parameter_value=j['parameter_value'])
                        new_vc_params.save()
                    logger.info(helper.generate_logging_message(user, 'vc api', 'PUT',
                                                                id, 'success', 'Success vc parameters inserted'))

            # update notifications
            vc_notifications = parameters.get('notifications', None)
            vc_original_notifications = Notification.query.filter(
                Notification.validation_check_id == id)

            original_notifications = []
            for i in vc_original_notifications:
                original_notifications.append(i.id)

            new_notifications = []
            for i in vc_notifications:
                if 'id' in i:
                    new_notifications.append(i['id'])

            for i in original_notifications:
                if i not in new_notifications:
                    item_delete = Notification.query.filter(Notification.id == i)
                    for i in item_delete:
                        db.session.delete(i)
                        db.session.commit()

            for i in vc_notifications:
                if i['type'] == '':
                    i['type'] = 'Email'
                if 'id' in i:
                    vc_notifications_update = Notification.query.get(i['id'])
                    vc_notifications_update.notify_if_error = i['notify_if_error']
                    vc_notifications_update.notify_if_failure = i['notify_if_failure']
                    vc_notifications_update.notify_if_success = i['notify_if_success']
                    vc_notifications_update.value = i['value']
                    vc_notifications_update.type = i['type']

                    vc_notifications_update.save()
                else:
                    vc_new_notifications = Notification(validation_check_id=id,
                                                        notify_if_error=i['notify_if_error'],
                                                        notify_if_failure=i['notify_if_failure'],
                                                        notify_if_success=i['notify_if_success'],
                                                        value=i['value'],
                                                        type=i['type'])

                    vc_new_notifications.save()

            for i in vc_original_notifications:
                if (i.notify_if_error is False) and (i.notify_if_failure is False) and (i.notify_if_success is False):
                    item_delete = Notification.query.filter(
                        Notification.id == i.id)
                    for j in item_delete:
                        db.session.delete(j)
                        db.session.commit()

            # update vc_keywords
            vc_keywords = parameters.get('keywords', None)
            vc_original_keywords = Keyword.query.filter(
                Keyword.validation_check_id == id)

            original_keywords = []
            for i in vc_original_keywords:
                original_keywords.append(i.id)

            new_keywords = []
            for i in vc_keywords:
                if 'id' in i:
                    new_keywords.append(i['id'])

            for i in original_keywords:
                if i not in new_keywords:
                    item_delete = Keyword.query.filter(Keyword.id == i)
                    for i in item_delete:
                        db.session.delete(i)
                        db.session.commit()

            for i in vc_keywords:
                if 'id' in i:
                    vc_keywords_update = Keyword.query.get(i['id'])
                    vc_keywords_update.keyword = i['keyword']
                    vc_keywords_update.save()
                else:
                    vc_new_keywords = Keyword(validation_check_id=id,
                                              keyword=i['keyword'])

                    vc_new_keywords.save()

            return vc_schema.jsonify(vc), 200

        else:
            params_invalid = []
            for i in vc_param_list:
                if i not in validator_list:
                    params_invalid.append(i)

            return jsonify({'Message': 'Invalid parameters found', 'Parameters': params_invalid}), 404
    else:
        return jsonify({'Message': 'No record found in Data Explorer for the given data set uuid: {}'.format(payload)}), 400

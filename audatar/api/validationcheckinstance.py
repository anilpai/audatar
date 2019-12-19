from flask import Blueprint, jsonify, request
import json
import logging

from audatar.models import ValidationCheckInstance, ValidationCheck
from audatar.serializers import vci_schema, vcis_schema
from audatar.extensions import db
from audatar.api import token_required
from flask_cors import CORS
from flasgger import swag_from

validation_check_instance_bp = Blueprint(
    'validation_check_instance_bp', __name__, url_prefix='/api/vci')

CORS(validation_check_instance_bp)


@validation_check_instance_bp.route('/', methods=['GET'])
@token_required
@swag_from('yml/validationcheckinstance_list.yml')
def list_of_validation_check_instances():
    """list all validation check instances."""
    parameters = request.args.to_dict(flat=True)

    ''' Filter conditions'''

    name_filter = parameters.get('name', None)
    start_date = parameters.get('start_date', None)
    end_date = parameters.get('end_date', None)

    ''' Filter by status & task_id'''
    status = parameters.get('status', None)
    task_id = parameters.get('task_id', None)
    sent_to_validation_registry = parameters.get('vr_sent', None)

    ''' Pagination parameters '''
    pageSize = parameters.get('pageSize', None)
    pageNumber = parameters.get('pageNumber', None)

    ''' Set defaults if not included in input, remove them so they are not included in filter'''
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
    order_queries = [ValidationCheckInstance.time_submitted.desc()]

    """ Filter name using a case-insensitive LIKE instead of EQUALS """
    if name_filter:
        """Remove name parameter so that we don't include an equal filter
        too."""
        name_filter = '%{0}%'.format(name_filter)
        parameters.pop('name')
        filter_queries.append(ValidationCheck.name.ilike(name_filter))
        order_queries.append(ValidationCheck.name)

    if start_date is not None:
        parameters.pop('start_date')
        filter_queries.append(ValidationCheckInstance.time_submitted >= start_date)

    if end_date is not None:
        parameters.pop('end_date')
        filter_queries.append(ValidationCheckInstance.time_submitted <= end_date)

    if task_id is not None:
        parameters.pop('task_id')
        filter_queries.append(ValidationCheckInstance.task_id == task_id)

    if status is not None:
        parameters.pop('status')
        filter_queries.append(ValidationCheckInstance.status == status)

    if sent_to_validation_registry is not None:
        parameters.pop('vr_sent')
        filter_queries.append(ValidationCheckInstance.sent_to_validation_registry == sent_to_validation_registry)

    vcis_all = ValidationCheckInstance.query.join(ValidationCheck, ValidationCheckInstance.validation_check_id == ValidationCheck.id)\
        .filter_by(**parameters).filter(*filter_queries).order_by(*order_queries)

    """ Paginate query """
    vcis_all = vcis_all.paginate(per_page=pageSize, error_out=True)

    """ Return no data if result = 0 """
    if vcis_all.total == 0:
        return jsonify(count=0, data=[]), 200

    """ Go to pageNumber if it's valid """
    if pageNumber > vcis_all.pages:
        return jsonify(msg='error', summary='Bad Request', detail=' Invalid page number {}'.format(pageNumber)), 400
    else:
        vcis_all = vcis_all.query.paginate(
            page=pageNumber, per_page=pageSize, error_out=True)

    result = vcis_schema.dump(vcis_all.items)
    return jsonify(pageSize=pageSize, pageNumber=pageNumber, count=vcis_all.total, data=result.data), 200


@validation_check_instance_bp.route('/<id>', methods=['GET'])
@token_required
@swag_from('yml/validationcheckinstance_by_id.yml')
def get_vci_by_id(id):
    """detailed validation check instance."""

    vci = ValidationCheckInstance.query.get(id)

    if not vci:
        return jsonify({'Message': 'Validation Check Instance doesnt exist'}), 404

    if vci.status != 'Error' and vci.result_records is not None:
        vci.result_records = json.loads(vci.result_records)
    vci.input = json.loads(vci.input)

    return vci_schema.jsonify(vci), 200


@validation_check_instance_bp.route('/<id>', methods=['DELETE'])
@token_required
# @swag_from('yml/validationcheckinstance_delete.yml')
def delete_vci(id):
    """delete validation check instance."""

    vci = ValidationCheckInstance.query.get(id)

    if vci is None:
        return jsonify({'Message': 'Validation Check Instance Not Found'}), 404

    vci.delete()
    return jsonify({'Message': 'Validation Check {0} successfully deleted'.format(vci.id)}), 200


@validation_check_instance_bp.route('/', methods=['POST'])
@token_required
@swag_from('yml/validationcheckinstance_post.yml')
def create_vci():
    """create validation check instance."""

    parameters = json.loads(request.data.decode('utf-8'))
    new_vci = ValidationCheckInstance(task_id=parameters.get('task_id', None),
                                      validation_check_id=parameters.get(
                                          'validation_check_id', None),
                                      input=parameters.get('input', None),
                                      time_submitted=parameters.get(
                                          'time_submitted', None),
                                      time_started=parameters.get(
                                          'time_started', None),
                                      time_completed=parameters.get(
                                          'time_completed', None),
                                      status=parameters.get('status', None),
                                      result_records=parameters.get(
                                          'result_records', None),
                                      result=parameters.get('result', None),
                                      result_count=parameters.get(
                                          'result_count', None),
                                      created_by=parameters.get('created_by', None),
                                      result_metric=parameters.get(
                                          'result_metric', None),
                                      sent_to_validation_registry=parameters.get('sent_to_validation_registry', False))
                                      
    new_vci.save()
    logging.info(new_vci)
    return vci_schema.jsonify(new_vci), 200


@validation_check_instance_bp.route('/task_id/<task_id>', methods=['PUT'])
@token_required
def update_vci_by_task_id(task_id):
    """parse request."""
    data_dict = json.loads(request.data.decode('utf-8'))

    """ If validation check instance entry missing in db """
    vcis_task = ValidationCheckInstance.query.filter(ValidationCheckInstance.task_id == task_id).one_or_none()
    if not vcis_task:
        return jsonify({'Task Id': task_id,
                        'Message': 'Validation Check Instance was not created, hence cant be updated'}), 404

    """ update instance status in the db """
    t_id = vcis_task.id
    ValidationCheckInstance.query.filter(ValidationCheckInstance.id == t_id).update(data_dict)
    db.session.flush()
    db.session.commit()

    """ return the instance """
    vci = ValidationCheckInstance.query.filter(
        ValidationCheckInstance.id == t_id).one_or_none()
    if vci.status != 'Error' and vci.result_records is not None:
        vci.result_records = json.loads(vci.result_records)
    vci.input = json.loads(vci.input)

    return vci_schema.jsonify(vci), 200


@validation_check_instance_bp.route('/<id>', methods=['PUT'])
@token_required
@swag_from('yml/validationcheckinstance_put.yml')
def update_vci_by_id(id):

    data_dict = json.loads(request.data.decode('utf-8'))

    """Retrieve VCI from database based on id"""
    vci = ValidationCheckInstance.query.get(id)
    if not vci:
        return jsonify({'Id': id,
                        'Message': 'Validation Check Instance was not created, hence cant be updated'}), 404

    """Update the VCI """
    ValidationCheckInstance.query.filter(ValidationCheckInstance.id == vci.id).update(data_dict)
    db.session.flush()
    db.session.commit()

    """ return the instance """
    updated_vci = ValidationCheckInstance.query.filter(
        ValidationCheckInstance.id == vci.id).one_or_none()

    if updated_vci.status != 'Error' and updated_vci.result_records is not None:
        updated_vci.result_records = json.loads(updated_vci.result_records)
    updated_vci.input = json.loads(updated_vci.input)

    return vci_schema.jsonify(updated_vci), 200

from flask import Blueprint, jsonify

from audatar.models import ValidationCheckParameters
from audatar.serializers import vcp_schema, vcps_schema
from audatar.extensions import auth
from audatar.api import token_required
from flask_cors import CORS

validation_check_parameters_bp = Blueprint(
    'validation_check_parameters_bp', __name__, url_prefix='/api/vcp')

CORS(validation_check_parameters_bp)


@validation_check_parameters_bp.route('/', methods=['GET'])
@token_required
def list_of_validaton_check_parameters():
    """list all validation check parameters."""
    vcps_all = ValidationCheckParameters.query.all()
    result = vcps_schema.dump(vcps_all)
    return jsonify(data=result.data), 200


@validation_check_parameters_bp.route('/<id>', methods=['GET'])
@token_required
def get_vcp_by_id(id):
    """detailed validation check parameters."""
    vcp = ValidationCheckParameters.query.get(id)
    if not vcp:
        return jsonify({'Validation Check Id': id,
                        'Message': 'Validation Check Parameters doesnt exist'}), 404
    return vcp_schema.jsonify(vcp), 200


@validation_check_parameters_bp.route('/vc_id/<vc_id>', methods=['GET'])
@token_required
def get_vcp_by_vc_id(vc_id):
    """detailed validation check parameters by vc id."""
    vcps_all = ValidationCheckParameters.query.filter(
        ValidationCheckParameters.validation_check_id == vc_id).all()
    if not vcps_all:
        return jsonify({'Validation Check Id': vc_id,
                        'Message': 'Validation Check Parameters doesnt exist'}), 404
    result = vcps_schema.dump(vcps_all)
    return jsonify(data=result.data), 200

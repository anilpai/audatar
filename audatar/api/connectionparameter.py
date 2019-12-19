from flask import Blueprint, jsonify

from audatar.models import ConnectionParameter
from audatar.serializers import conn_parameters_schema, conns_parameters_schema
from audatar.api import token_required
from flask_cors import CORS

connection_parameter_bp = Blueprint(
    'connection_parameter_bp', __name__, url_prefix='/api/cp')

CORS(connection_parameter_bp)


@connection_parameter_bp.route('/', methods=['GET'])
@token_required
def list_all_connection_parameters():
    """list all connections parameters."""
    conns_all = ConnectionParameter.query.all()
    result = conns_parameters_schema.dump(conns_all)
    return jsonify(data=result.data), 200


@connection_parameter_bp.route('/<id>', methods=['GET'])
@token_required
def get_cp_by_id(id):
    """get connection parameters by id."""
    conn = ConnectionParameter.query.get(id)
    if not conn:
        return jsonify({'Id': id,
                        'Message': 'Connection Parameter doesnt exist'}), 404
    return conn_parameters_schema.jsonify(conn), 200

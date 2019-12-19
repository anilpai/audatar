from flask import Blueprint, jsonify, request
import json

from audatar.models import ConnectionType
from audatar.serializers import conns_type, conn_type
from audatar.extensions import db, auth
from audatar.api import token_required
from flask_cors import CORS

connectiontype_bp = Blueprint('connectiontype_bp', __name__, url_prefix='/api/connectiontype')

CORS(connectiontype_bp)


@connectiontype_bp.route('/', methods=['GET'])
@token_required
def list_of_connectionstype():
    """list all connections type."""
    parameters = request.args.to_dict(flat=True)
    connectiontype_all = ConnectionType.query.filter_by(**parameters).all()
    result = conns_type.dump(connectiontype_all)
    return jsonify(data=result.data), 200


@connectiontype_bp.route('/<id>', methods=['GET'])
@token_required
def get_connectiontype_by_id(id):
    """detailed connectiontype by id."""
    connectiontype = ConnectionType.query.get(id)
    if not connectiontype:
        return jsonify({'Id': id,
                        'Message': 'Connection Type doesnt exist'}), 404
    return conn_type.jsonify(connectiontype), 200

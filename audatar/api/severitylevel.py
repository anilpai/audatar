from flask import Blueprint, jsonify, request
import json

from audatar.models import SeverityLevel
from audatar.serializers import severitylevel_schema, severitylevels_schema
from audatar.extensions import db, auth
from audatar.api import token_required
from flask_cors import CORS

severitylevel_bp = Blueprint(
    'severitylevel_bp', __name__, url_prefix='/api/severitylevel')

CORS(severitylevel_bp)


@severitylevel_bp.route('/', methods=['GET'])
@token_required
def list_of_severitylevels():
    """list all severitylevels."""
    parameters = request.args.to_dict(flat=True)
    severitylevels_all = SeverityLevel.query.filter_by(**parameters).all()
    result = severitylevels_schema.dump(severitylevels_all)
    return jsonify(count=len(severitylevels_all), data=result.data), 200


@severitylevel_bp.route('/<id>', methods=['GET'])
@token_required
def get_severitylevel_by_id(id):
    """detailed severitylevel by id."""
    severitylevel = SeverityLevel.query.get(id)
    if not severitylevel:
        return jsonify({'Id': id,
                        'Message': 'Severity Level doesn\'t exist'}), 404
    return severitylevel_schema.jsonify(severitylevel), 200


@severitylevel_bp.route('/', methods=['POST'])
@token_required
def create_severitylevel():
    """create severitylevel."""

    parameters = json.loads(request.data.decode('utf-8'))
    new_severitylevel = SeverityLevel(parameters)
    db.session.add(new_severitylevel)
    db.session.commit()
    return severitylevel_schema.jsonify(new_severitylevel), 200


@severitylevel_bp.route('/<id>', methods=['DELETE'])
@token_required
def delete_severitylevel(id):
    """delete severitylevel."""

    severitylevel = SeverityLevel.query.get(id)
    if severitylevel is None:
        return jsonify({'Message': 'Severity Level Not Found'}), 404
    else:
        db.session.delete(severitylevel)
        db.session.commit()
        return jsonify({'Message': 'Severity Level {0} successfully deleted'.format(severitylevel.id)}), 200

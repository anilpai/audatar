from flask import Blueprint, jsonify, request
import json

from audatar.models import Dimension
from audatar.serializers import dimension_schema, dimensions_schema
from audatar.extensions import db, auth
from audatar.api import token_required
from flask_cors import CORS

dimension_bp = Blueprint(
    'dimension_bp', __name__, url_prefix='/api/dimension')

CORS(dimension_bp)


@dimension_bp.route('/', methods=['GET'])
@token_required
def list_of_dimensions():
    """list all dimensions."""
    parameters = request.args.to_dict(flat=True)
    dimensions_all = Dimension.query.filter_by(**parameters).all()
    result = dimensions_schema.dump(dimensions_all)
    return jsonify(count=len(dimensions_all), data=result.data), 200


@dimension_bp.route('/<id>', methods=['GET'])
@token_required
def get_dimension_by_id(id):
    """detailed dimension by id."""
    dimension = Dimension.query.get(id)
    if not dimension:
        return jsonify({'Id': id,
                        'Message': 'Dimension doesn\'t exist'}), 404
    return dimension_schema.jsonify(dimension), 200


@dimension_bp.route('/', methods=['POST'])
@token_required
def create_dimension():
    """create dimension."""

    parameters = json.loads(request.data.decode('utf-8'))
    new_dimension = Dimension(parameters)
    db.session.add(new_dimension)
    db.session.commit()
    return dimension_schema.jsonify(new_dimension), 200


@dimension_bp.route('/<id>', methods=['DELETE'])
@token_required
def delete_dimension(id):
    """delete dimension."""

    dimension = Dimension.query.get(id)
    if dimension is None:
        return jsonify({'Message': 'Dimension Not Found'}), 404
    else:
        db.session.delete(dimension)
        db.session.commit()
        return jsonify({'Message': 'Dimension {0} successfully deleted'.format(dimension.id)}), 200

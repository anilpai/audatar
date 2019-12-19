from flask import Blueprint, jsonify
import json

from audatar.models import Validator
from audatar.serializers import validator_schema, validators_schema
from audatar.extensions import auth
from audatar.api import token_required
from audatar.utils.helper import get_class_by_class_path
from flask_cors import CORS

validator_bp = Blueprint('validator_bp', __name__, url_prefix='/api/validator')

CORS(validator_bp)


@validator_bp.route('/', methods=['GET'])
@token_required
def list_of_validators():
    """list all validators."""
    validator_all = Validator.query.all()
    result = validators_schema.dump(validator_all)
    return jsonify(data=result.data), 200


@validator_bp.route('/<id>', methods=['GET'])
@token_required
def get_validator_by_id(id):
    """detailed validator by id."""
    validator = Validator.query.get(id)

    if not validator:
        return jsonify({'Id': id,
                        'Message': 'Validator doesnt exist'}), 404

    validator_class = get_class_by_class_path(validator.class_path)
    ui_fields = validator_class.ui_fields()
    fields = []
    for field in ui_fields:
        field_dict = {}
        field_type = field.__class__.__name__
        options = None
        if(field_type == 'ConnectionField'):
            options = []
            connections = field.connections()
            for connection in connections:
                options.append({'value': connection.name, 'display': connection.name})
        elif(field_type == 'SelectField'):
            options = []
            for value, display in field.selection_list():
                options.append({'value': value, 'display': display})
            field_dict['allow_multiple'] = field.allow_multiple()
        elif(field_type == 'TextAreaField'):
            field_dict['rows'] = field.rows()
            field_dict['placeholder'] = field.placeholder()
        field_dict['type'] = field_type
        field_dict['parameter_name'] = field.parameter_name()
        field_dict['label'] = field.label()
        field_dict['description'] = field.description()
        field_dict['default_value'] = field.default_value()
        if options:
            field_dict['options'] = options
        fields.append(field_dict)

    required_list = [req[0] for req in validator_class.required_parameters()]

    validator = json.loads(validator_schema.dumps(validator)[0])
    validator['fields'] = fields
    validator['required_parameters'] = required_list
    return jsonify(validator), 200

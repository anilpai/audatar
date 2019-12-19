from flask import Blueprint, jsonify, request
import json

from audatar.models import NotificationLog
from audatar.serializers import nl_schema, nls_schema
from audatar.extensions import db, auth
from audatar.api import token_required
from flask_cors import CORS

notification_log_bp = Blueprint(
    'notification_log_bp', __name__, url_prefix='/api/nlog')

CORS(notification_log_bp)


@notification_log_bp.route('/', methods=['GET'])
@token_required
def list_of_notification_log_checks():
    """list all notification logs."""
    parameters = request.args.to_dict(flat=True)

    nls_all = NotificationLog.query.filter_by(**parameters).order_by('id')

    result = nls_schema.dump(nls_all)
    return jsonify(data=result.data), 200


@notification_log_bp.route('/<id>', methods=['GET'])
@token_required
def get_nl_by_id(id):
    """detailed validation check."""
    nf = NotificationLog.query.get(id)
    if not nf:
        return jsonify({'Id': id,
                        'Message': 'Notification doesnt exist'}), 404
    return nl_schema.jsonify(nf), 200


@notification_log_bp.route('/', methods=['POST'])
@token_required
def create_nl():
    """create notification log."""

    parameters = json.loads(request.data.decode('utf-8'))

    new_nl = NotificationLog(task_id=parameters.get('task_id', None), validation_check_id=parameters.get('validation_check_id', None),
                             time_completed=parameters.get('time_completed', None), value=parameters.get('value', None), type=parameters.get('type', None))

    db.session.add(new_nl)
    db.session.commit()
    return nl_schema.jsonify(new_nl), 200

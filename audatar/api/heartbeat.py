from flask import Blueprint, jsonify, request
import json
from audatar.models import Heartbeat
from audatar.serializers import heartbeat_schema, heartbeats_schema
from audatar.extensions import db, auth
from audatar.api import token_required
from flask_cors import CORS
from datetime import datetime

heartbeat_bp = Blueprint('heartbeat_bp', __name__, url_prefix='/api/heartbeat')

CORS(heartbeat_bp)


@heartbeat_bp.route('/', methods=['GET'])
@token_required
def get_latest_heartbeat():
    """Query heartbeat table for latest record."""

    heartbeat_max = Heartbeat.query.order_by(Heartbeat.time.desc()).first()
    result = heartbeat_schema.dump(heartbeat_max)

    return jsonify(result.data), 200


@heartbeat_bp.route('/', methods=['POST'])
@token_required
def create_heartbeat():
    """create heartbeat."""

    parameters = json.loads(request.data.decode('utf-8'))
    new_heartbeat = Heartbeat(time=datetime.now(), interval=parameters['interval'])
    db.session.add(new_heartbeat)
    db.session.commit()
    return heartbeat_schema.jsonify(new_heartbeat), 200

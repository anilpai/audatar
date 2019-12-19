from audatar.extensions import db, auth
from flask import Blueprint, jsonify, request
from flask_cors import CORS
from audatar.api import token_required
import subprocess

workers_bp = Blueprint('workers_bp', __name__, url_prefix='/api/workers')

CORS(workers_bp)


@workers_bp.route('/', methods=['GET'])
@token_required
def get_workers_online():
    """Show workers online."""
    cmd = 'celery -A audatar.task_executor status -C'
    output = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE).communicate()[0]

    try:
        output = output.decode('utf-8')
        output = output.replace('.', '')
        return jsonify({'message': output}), 200
    except Exception as e:
        return jsonify(flag='fail', msg=str(e)), 401

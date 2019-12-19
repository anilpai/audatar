from flask import Blueprint, jsonify, request
import json
from audatar.models import Connection
from audatar.serializers import conn_schema, conns_schema
from audatar.extensions import db, auth
from audatar.api import token_required
from flask_cors import CORS

connection_bp = Blueprint('connection_bp', __name__,
                          url_prefix='/api/connection')

CORS(connection_bp)


@connection_bp.route('/', methods=['GET'])
@token_required
def list_of_connections():
    """list all connections."""
    parameters = request.args.to_dict(flat=True)

    """ Pagination parameters """
    pageSize = parameters.get('pageSize', None)
    pageNumber = parameters.get('pageNumber', None)

    """ Set defaults if not included in input, remove them so they are not included in filter"""
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

    conns_all = Connection.query.filter_by(**parameters).order_by('name')

    """ Paginate query """
    conns_all = conns_all.paginate(per_page=pageSize, error_out=True)

    """ Return no data if result = 0 """
    if conns_all.total == 0:
        return jsonify(count=0, data=[]), 200

    """ Go to pageNumber if it's valid """
    if pageNumber > conns_all.pages:
        return jsonify(msg='error', summary='Bad Request', detail=' Invalid page number {}'.format(pageNumber)), 400
    else:
        conns_all = conns_all.query.paginate(
            page=pageNumber, per_page=pageSize, error_out=True)

    result = conns_schema.dump(conns_all.items)
    return jsonify(pageSize=pageSize, pageNumber=pageNumber, count=conns_all.total, data=result.data), 200


@connection_bp.route('/<id>', methods=['GET'])
@token_required
def get_connection_by_id(id):
    """detailed connections."""
    conn = Connection.query.get(id)
    if not conn:
        return jsonify({'Id': id,
                        'Message': 'Connection doesnt exist'}), 404
    return conn_schema.jsonify(conn), 200


@connection_bp.route('/', methods=['POST'])
@token_required
def create_conn():
    """create connection."""

    parameters = json.loads(request.data.decode('utf-8'))
    new_conn = Connection(name=parameters['name'], description=parameters['description'],
                          connection_type_id=parameters['connection_type_id'])
    db.session.add(new_conn)
    db.session.commit()
    return conn_schema.jsonify(new_conn), 200


@connection_bp.route('/<id>', methods=['DELETE'])
@token_required
def delete_conn(id):
    """delete connection."""

    conn = Connection.query.get(id)
    if conn is None:
        return jsonify({'Message': 'Connection Not Found'}), 404
    else:
        db.session.delete(conn)
        db.session.commit()
        return jsonify({'Message': 'Validation Check {0} successfully deleted'.format(conn.id)}), 200

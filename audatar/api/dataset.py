from flask import Blueprint, jsonify, request
from audatar.api import token_required
from flask_cors import CORS
from audatar.extensions import index

dataset_bp = Blueprint('dataset_bp', __name__, url_prefix='/api/dataset')

CORS(dataset_bp)


@dataset_bp.route('/', methods=['GET'])
@token_required
def list_of_dataset_suggestions():
    """list all dataset name suggestions with corresponding uuid."""
    parameters = request.args.to_dict(flat=True)

    res = index.search(
        parameters.get('s', ' '),
        {"attributesToRetrieve": "name,uuid,database", "hitsPerPage": 20}
    )

    for i in res['hits']:
        del i['objectID']
        del i['_highlightResult']

    return jsonify(data=res['hits'], count=len(res['hits'])), 200


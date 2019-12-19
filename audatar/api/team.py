from flask import Blueprint, jsonify, request
import json

from audatar.models import Team
from audatar.serializers import team_schema, teams_schema
from audatar.extensions import db, auth
from audatar.api import token_required
from flask_cors import CORS

team_bp = Blueprint('team_bp', __name__, url_prefix='/api/team')

CORS(team_bp)


@team_bp.route('/', methods=['GET'])
@token_required
def list_of_teams():
    """list all teams."""
    parameters = request.args.to_dict(flat=True)
    teams_all = Team.query.filter_by(**parameters).all()
    result = teams_schema.dump(teams_all)
    return jsonify(count=len(teams_all), data=result.data), 200


@team_bp.route('/<id>', methods=['GET'])
@token_required
def get_team_by_id(id):
    """detailed team by id."""
    team = Team.query.get(id)
    if not team:
        return jsonify({'Id': id,
                        'Message': 'Team doesnt exist'}), 404
    return team_schema.jsonify(team), 200


@team_bp.route('/', methods=['POST'])
@token_required
def create_team():
    """create team."""
    parameters = json.loads(request.data.decode('utf-8'))

    new_team = Team(name=parameters['name'], description=parameters['description'], is_admin=parameters['is_admin'])
    db.session.add(new_team)
    db.session.commit()

    return team_schema.jsonify(new_team), 200


@team_bp.route('/<id>', methods=['DELETE'])
@token_required
def delete_team(id):
    """delete team."""

    team = Team.query.get(id)
    if team is None:
        return jsonify({'Message': 'Team Not Found'}), 404
    else:
        db.session.delete(team)
        db.session.commit()
        return jsonify({'Message': 'Team {0} successfully deleted'.format(team.id)}), 200

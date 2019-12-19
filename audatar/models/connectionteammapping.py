from audatar.extensions import db


class ConnectionTeamMapping(db.Model):
    __tablename__ = 'connectionteammappings'
    id = db.Column(db.Integer, primary_key=True)
    connection_id = db.Column(db.Integer, db.ForeignKey('connections.id'))
    connection = db.relationship('Connection')
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    team = db.relationship('Team')

    def __init__(self, connection_id=None, team_id=None):
        self.connection_id = connection_id
        self.team_id = team_id

    def __repr__(self):
        return '<connection team Mapping %r>' % (self.id)

    def to_dict(self):
        return {
            'id': self.id,
            'connection_id': self.connection_id,
            'team_id': self.team_id
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

from audatar.extensions import db


class ConnectionParameter(db.Model):
    __tablename__ = 'connectionparameters'
    id = db.Column(db.Integer, primary_key=True)
    connection_id = db.Column(db.Integer, db.ForeignKey('connections.id'))
    connection = db.relationship('Connection')
    parameter_name = db.Column(db.String(64), unique=True)
    parameter_value = db.Column(db.String(256))

    def __init__(self, connection_id=None, parameter_name=None, parameter_value=None):
        self.connection_id = connection_id
        self.parameter_name = parameter_name
        self.parameter_value = parameter_value

    def __repr__(self):
        return '<connectionparameter %r>' % (self.id)

    def to_dict(self):
        return {
            'id': self.id,
            'connection_id': self.connection_id,
            'parameter_name': self.parameter_name,
            'parameter_value': self.parameter_value
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

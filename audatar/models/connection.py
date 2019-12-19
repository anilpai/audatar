from audatar.extensions import db


class Connection(db.Model):
    __tablename__ = 'connections'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    description = db.Column(db.String(256))
    connection_type_id = db.Column(db.Integer, db.ForeignKey('connectiontypes.id'))

    def __init__(self, name=None, description=None, connection_type_id=None):
        self.name = name
        self.description = description
        self.connection_type_id = connection_type_id

    def __repr__(self):
        return '<connection %r>' % (self.name)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'connection_type_id': self.connection_type_id
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

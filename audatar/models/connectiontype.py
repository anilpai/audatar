from audatar.extensions import db


class ConnectionType(db.Model):
    __tablename__ = 'connectiontypes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    class_path = db.Column(db.String(256))

    def __init__(self, name=None, class_path=None):
        self.name = name
        self.class_path = class_path

    def __repr__(self):
        return '<connectiontype %r>' % (self.name)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'class_path': self.class_path
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

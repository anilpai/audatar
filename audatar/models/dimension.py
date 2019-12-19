from audatar.extensions import db


class Dimension(db.Model):
    __tablename__ = 'dimensions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    description = db.Column(db.String(256))

    def __repr__(self):
        return '<dimension %r>' % (self.name)

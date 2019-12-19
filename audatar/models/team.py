from audatar.extensions import db


class Team(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    description = db.Column(db.String(256))
    is_admin = db.Column(db.BOOLEAN(), nullable=False, default=False)

    def __repr__(self):
        return '<team %r>' % (self.name)

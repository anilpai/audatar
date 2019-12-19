from audatar.extensions import db


class SeverityLevel(db.Model):
    __tablename__ = 'severitylevels'
    id = db.Column(db.Integer, primary_key=True)
    severity_level_order = db.Column(db.Integer)
    name = db.Column(db.String(128), unique=True)
    description = db.Column(db.String(256))

    def __repr__(self):
        return '<severitylevel %r>' % (self.name)

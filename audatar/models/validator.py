from audatar.extensions import db


class Validator(db.Model):
    __tablename__ = 'validators'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    description = db.Column(db.String(256))
    class_path = db.Column(db.String(256))

    def __repr__(self):
        return "<validator(id='%s')>" % self.id

from audatar.extensions import db


class Jwtblacklist(db.Model):
    __tablename__ = 'jwtblacklist'
    token = db.Column(db.Text)
    expiration = db.Column(db.DateTime, primary_key=True)

    def __init__(self, token=None, expiration=None):
        self.token = token
        self.expiration = expiration

    def __repr__(self):
        return '<Jwtblacklist %r>' % (self.token)

    def to_dict(self):
        return {
            'token': self.token,
            'expiration': self.expiration
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

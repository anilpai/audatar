from audatar.extensions import db


class Heartbeat(db.Model):
    __tablename__ = 'heartbeat'
    time = db.Column(db.DateTime, primary_key=True)
    interval = db.Column(db.Integer)

    def __init__(self, time=None, interval=None):
        self.time = time
        self.interval = interval

    def __repr__(self):
        return '<Heartbeat %r>' % (self.time)

    def to_dict(self):
        return {
            'time': self.time,
            'interval': self.interval
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

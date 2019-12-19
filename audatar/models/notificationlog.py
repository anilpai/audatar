from audatar.extensions import db


class NotificationLog(db.Model):
    __tablename__ = 'notificationlogs'
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.String(128))
    validation_check_id = db.Column(db.Integer, db.ForeignKey('validationchecks.id'))
    time_completed = db.Column(db.DateTime)
    value = db.Column(db.String(256))
    type = db.Column(db.String(256))

    def __init__(self, task_id=None, validation_check_id=None,
                 time_completed=None, value=None, type=None):
        self.task_id = task_id
        self.validation_check_id = validation_check_id
        self.time_completed = time_completed
        self.value = value
        self.type = type

    def __repr__(self):
        return '<notification_logs %r>' % (self.id)

    def to_dict(self):
        return {
            'id': self.id,
            'task_id': self.task_id,
            'validation_check_id': self.validation_check_id,
            'time_completed': self.time_completed,
            'value': self.value,
            'type': self.type
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

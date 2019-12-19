from audatar.extensions import db


class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    validation_check_id = db.Column(db.Integer, db.ForeignKey('validationchecks.id'))
    validation_check = db.relationship('ValidationCheck', backref='notifications')
    notify_if_failure = db.Column(db.BOOLEAN(), nullable=False, default=False)
    notify_if_success = db.Column(db.BOOLEAN(), nullable=False, default=False)
    notify_if_error = db.Column(db.BOOLEAN(), nullable=False, default=False)
    value = db.Column(db.String(256))
    type = db.Column(db.String(256))
    time_updated = db.Column(db.DateTime)
    updated_by = db.Column(db.String(128))

    def __repr__(self):
        return '<notification %r>' % (self.id)

    def __init__(self, validation_check_id=None,
                 notify_if_failure=None, notify_if_success=None,
                 notify_if_error=None, value=None, type=None, time_updated=None, updated_by=None):
        self.validation_check_id = validation_check_id
        self.notify_if_failure = notify_if_failure
        self.notify_if_success = notify_if_success
        self.notify_if_error = notify_if_error
        self.value = value
        self.type = type
        self.time_updated = time_updated
        self.updated_by = updated_by

    def to_dict(self):
        return {
            'id': self.id,
            'validation_check_id': self.validation_check_id,
            'notify_if_failure': self.notify_if_failure,
            'notify_if_success': self.notify_if_success,
            'notify_if_error': self.notify_if_error,
            'value': self.value,
            'type': self.type,
            'time_updated': self.time_updated,
            'updated_by': self.updated_by
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

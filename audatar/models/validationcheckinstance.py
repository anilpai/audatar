from audatar.extensions import db


class ValidationCheckInstance(db.Model):
    __tablename__ = 'validationcheckinstances'
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.String(128))
    validation_check_id = db.Column(db.Integer, db.ForeignKey('validationchecks.id'))
    validation_check = db.relationship('ValidationCheck')
    input = db.Column(db.Text)
    time_submitted = db.Column(db.DateTime)
    time_started = db.Column(db.DateTime)
    time_completed = db.Column(db.DateTime)
    status = db.Column(db.String(128))
    result_records = db.Column(db.Text)
    result = db.Column(db.String(128))
    result_count = db.Column(db.Integer)
    created_by = db.Column(db.String(128))
    result_metric = db.Column(db.Text)
    sent_to_validation_registry = db.Column(db.BOOLEAN())

    def __init__(self, task_id=None, validation_check_id=None,
                 input=None, time_submitted=None,
                 time_started=None, time_completed=None,
                 status=None, result_records=None, result=None,
                 result_count=None, created_by=None,
                 result_metric=None, sent_to_validation_registry=None):

        self.task_id = task_id
        self.validation_check_id = validation_check_id
        self.input = input
        self.time_submitted = time_submitted
        self.time_started = time_started
        self.time_completed = time_completed
        self.status = status
        self.result_records = result_records
        self.result = result
        self.result_count = result_count
        self.created_by = created_by
        self.result_metric = result_metric
        self.sent_to_validation_registry = sent_to_validation_registry

    def __repr__(self):
        return "<VCInstance(id='%s')>" % self.id

    def to_dict(self):
        return {
            'id': self.id,
            'task_id': self.task_id,
            'validation_check_id': self.validation_check_id,
            'input': self.input,
            'time_submitted': self.time_submitted,
            'time_started': self.time_started,
            'status': self.status,
            'created_by': self.created_by,
            'result_metric': self.result_metric,
            'sent_to_validation_registry': self.sent_to_validation_registry
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

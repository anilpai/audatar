from audatar.extensions import db


class ValidationCheckParameters(db.Model):
    __tablename__ = 'validationcheckparameters'
    id = db.Column(db.Integer, primary_key=True)
    validation_check_id = db.Column(db.Integer, db.ForeignKey('validationchecks.id'))
    validation_check = db.relationship('ValidationCheck', backref='parameters')
    parameter_name = db.Column(db.Text)
    parameter_value = db.Column(db.Text)
    time_updated = db.Column(db.DateTime)
    updated_by = db.Column(db.String(128))

    def __init__(self, validation_check_id=None, parameter_name=None, parameter_value=None, time_updated=None, updated_by=None):
        self.validation_check_id = validation_check_id
        self.parameter_name = parameter_name
        self.parameter_value = parameter_value
        self.time_updated = time_updated
        self.updated_by = updated_by

    def __repr__(self):
        return '<VCParam %r>' % (self.id)

    def to_dict(self):
        return {
            'id': self.id,
            'validation_check_id': self.validation_check_id,
            'parameter_name': self.parameter_name,
            'parameter_value': self.parameter_value,
            'time_updated': self.time_updated,
            'updated_by': self.updated_by
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

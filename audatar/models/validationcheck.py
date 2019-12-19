from audatar.extensions import db


class ValidationCheck(db.Model):
    __tablename__ = 'validationchecks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    is_active = db.Column(db.BOOLEAN(), nullable=False, default=False)
    validator_id = db.Column(db.Integer, db.ForeignKey('validators.id'))
    validator = db.relationship('Validator')
    vc = db.relationship('ValidationCheckInstance', backref='vc')
    description = db.Column(db.String(256))
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    team = db.relationship('Team', backref='team')
    dataset_id = db.Column(db.String(256))
    dimension_id = db.Column(db.Integer, db.ForeignKey('dimensions.id'))
    dimension = db.relationship('Dimension')
    severity_level_id = db.Column(db.Integer, db.ForeignKey('severitylevels.id'))
    severity_level = db.relationship('SeverityLevel')
    documentation_url = db.Column(db.String(256))
    cron_schedule = db.Column(db.String(64))
    time_updated = db.Column(db.DateTime)
    updated_by = db.Column(db.String(128))
    tags = db.Column(db.String(128))

    def __init__(self, name=None, is_active=None, validator_id=None,
                 description=None, team_id=None, dataset_id=None,
                 dimension_id=None, severity_level_id=None,
                 documentation_url=None, cron_schedule=None,
                 time_updated=None, updated_by=None, tags=None):
        self.name = name
        self.is_active = is_active
        self.validator_id = validator_id
        self.description = description
        self.team_id = team_id
        self.dataset_id = dataset_id
        self.dimension_id = dimension_id
        self.severity_level_id = severity_level_id
        self.documentation_url = documentation_url
        self.cron_schedule = cron_schedule
        self.time_updated = time_updated
        self.updated_by = updated_by
        self.tags = tags

    def __repr__(self):
        return "<VC(id='%s')>" % self.id

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'is_active': self.is_active,
            'validator_id': self.validator_id,
            'description': self.description,
            'team_id': self.team_id,
            'dataset_id': self.dataset_id,
            'dimension_id': self.dimension_id,
            'severity_level_id': self.severity_level_id,
            'documentation_url': self.documentation_url,
            'cron_schedule': self.cron_schedule,
            'time_updated': self.time_updated,
            'updated_by': self.updated_by,
            'tags': self.tags
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

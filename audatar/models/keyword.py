from audatar.extensions import db


class Keyword(db.Model):
    __tablename__ = 'keywords'
    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(128), unique=True)
    validation_check_id = db.Column(db.Integer, db.ForeignKey('validationchecks.id'))
    validation_check = db.relationship('ValidationCheck', backref='keywords')

    def __init__(self, validation_check_id=None, keyword=None):
        self.validation_check_id = validation_check_id
        self.keyword = keyword

    def __repr__(self):
        return '<keyword %r>' % (self.keyword)

    def to_dict(self):
        return {
            'id': self.id,
            'validation_check_id': self.validation_check_id,
            'keyword': self.keyword
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

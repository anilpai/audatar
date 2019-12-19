from audatar.extensions import db


class Validgroups(db.Model):
    __tablename__ = 'validgroups'
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(128))

    def __init__(self, group_name=None):
        self.group_name = group_name

    def __repr__(self):
        return self.group_name

    def to_dict(self):
        return {
            'id': self.id,
            'group_name': self.group_name
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

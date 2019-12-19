# from audatar.extensions import db


'''DATASET MODEL IS DEPRECATED'''


# class DataSet(db.Model):
#     __tablename__ = 'datasets'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(128), unique=True)
#     description = db.Column(db.String(256))
#
#     def __init__(self, name=None, description=None):
#         self.name = name
#         self.description = description
#
#     def __repr__(self):
#         return '<DataSet %r>' % (self.name)
#
#     def to_dict(self):
#         return {
#             'id': self.id,
#             'name': self.name,
#             'description': self.description
#         }
#
#     def save(self):
#         db.session.add(self)
#         db.session.commit()
#
#     def delete(self):
#         db.session.delete(self)
#         db.session.commit()

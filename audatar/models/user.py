from audatar.extensions import db
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
import logging
from audatar import audatar_config


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.String(128))

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=None):
        _serializer = Serializer(audatar_config.secret_key, expires_in=expiration)
        return _serializer.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        _serializer = Serializer(audatar_config.secret_key)

        try:
            data = _serializer.loads(token)
        except SignatureExpired:
            logging.info('Valid token, but required')
            return None
        except BadSignature:
            logging.info('Invalid token')
            return None

        return User.query.get(data['id'])

    def __repr__(self):
        return '<User name: %r>' % (self.username)

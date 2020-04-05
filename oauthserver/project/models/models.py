from project import db, bcrypt
from authlib.integrations.sqla_oauth2 import OAuth2ClientMixin


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False)
    firstname = db.Column(db.String(32))
    lastname = db.Column(db.String(32))
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(128), unique=True, nullable=True)

    def get_user_id(self):
        return self.id

    def get_user_name(self):
        return self.username

    def get_user_email(self):
        return self.email


class Client(db.Model, OAuth2ClientMixin):
    name = db.Column(db.String(40))
    description = db.Column(db.String(400))
    user_id = db.Column(db.ForeignKey('user.id'))
    user = db.relationship('User')
    client_id = db.Column(db.String(40), primary_key=True)
    client_secret = db.Column(db.String(55), unique=True, index=True, nullable=False)
    is_confidential = db.Column(db.Boolean)
    _redirect_uris = db.Column(db.Text)
    _default_scopes = db.Column(db.Text)
    #
    # @property
    # def client_type(self):
    #     if self.is_confidential:
    #         return 'confidential'
    #     return 'public'
    #
    # @property
    # def redirect_uris(self):
    #     if self._redirect_uris:
    #         return self._redirect_uris.split()
    #     return []
    #
    # @property
    # def default_redirect_uri(self):
    #     return self.redirect_uris[0]
    #
    # @property
    # def default_scopes(self):
    #     if self._default_scopes:
    #         return self._default_scopes.split()
    #     return []


class GrantToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    user = db.relationship('User')
    client_id = db.Column(db.String(40), db.ForeignKey('client.client_id'), nullable=False, )
    client = db.relationship('Client')
    code = db.Column(db.String(255), index=True, nullable=False)
    redirect_uri = db.Column(db.String(255))
    expires = db.Column(db.DateTime)
    _scopes = db.Column(db.Text)

    # To auto delete grants token
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    @property
    def scopes(self):
        if self._scopes:
            return self._scopes.split()
        return []


class Token(db.Model, OAuth2TokenMixin):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(
        db.String(40), db.ForeignKey('client.client_id'),
        nullable=False,
    )
    client = db.relationship('Client')

    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id')
    )
    user = db.relationship('User')
    token_type = db.Column(db.String(40))
    access_token = db.Column(db.String(255), unique=True)
    refresh_token = db.Column(db.String(255), unique=True)
    expires = db.Column(db.DateTime)
    _scopes = db.Column(db.Text)

    # # This is to auto delete a bearer token
    # def delete(self):
    #     db.session.delete(self)
    #     db.session.commit()
    #     return self
    #
    # @property
    # def scopes(self):
    #     if self._scopes:
    #         return self._scopes.split()
    #     return []

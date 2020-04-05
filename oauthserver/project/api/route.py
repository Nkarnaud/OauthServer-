from flask import request, render_template, Blueprint, jsonify
from .oauth import auth_server
from .models.models import User, Client


auth_endpoint = Blueprint(__name__, 'home')


def get_current_user():
    if 'id' in session:
        uid = session['id']
        return User.query.get(uid)
    return None


@auth_endpoint('/oauthserver/authorize', method=['GET', 'POST'])
def auth_handler():
    user = get_current_user()
    if request.method == 'GET':
        try:
            grant = auth_server.validate_consent_request(end_user=user)
        except OAuth2Error as error:
            return error.error
        return render_template('authorize.html', user=user, grant=grant)
    if not user and 'username' in request.form:
        username = request.form.get('username')
        user = User.query.filter_by(username=username).first()
    if request.form['confirm']:
        grant_user = user
    else:
        grant_user = None
    return auth_server.create_authorization_response(grant_user=grant_user)

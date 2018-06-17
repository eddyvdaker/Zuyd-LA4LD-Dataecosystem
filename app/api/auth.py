# -*- coding: utf-8 -*-
"""
    app.api.auth
    ~~~~~~~~~~~~

    Handles API authentication
"""
from flask import g, current_app
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth

from app.api.errors import error_response
from app.models import User, ApiKey

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()


@basic_auth.verify_password
def verify_password(username, password):
    """Verify if username password combination is correct"""
    user = User.query.filter_by(username=username).first()
    if user is None:
        return False
    g.current_user = user
    return user.check_password(password)


@basic_auth.error_handler
def basic_auth_error():
    """Basic API error"""
    return error_response(401)


@token_auth.verify_token
def verify_token(token):
    """Verify supplied token"""
    if ApiKey.query.filter_by(key=token).all():
        g.current_user = User.query.filter_by(
            username=current_app.config['SYSTEM_ACCOUNT']
        ).first()
    else:
        g.current_user = User.check_token(token) if token else None
    return g.current_user is not None


@token_auth.error_handler
def token_auth_error():
    """Handle token incorrect (or not existing) error"""
    return error_response(401)

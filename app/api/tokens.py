# -*- coding: utf-8 -*-
"""
    app.api.tokens
    ~~~~~~~~~~~~~~

    API token handling
"""
from flask import jsonify, g
from app import db

from app.api import bp
from app.api.auth import basic_auth, token_auth


@bp.route('/api/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    """Generate a token"""
    token = g.current_user.get_token()
    db.session.commit()
    return jsonify({'token': token})


@bp.route('/api/tokens', methods=['DELETE'])
@token_auth.login_required
def revoke_token():
    """Revoke a token"""
    g.current_user.revoke_token()
    db.session.commit()
    return '', 204

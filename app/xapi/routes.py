# -*- coding: utf-8 -*-
"""
    xapi.routes
    ~~~~~~~~~~~

    Routes used for handeling xAPI data.
"""

from flask import jsonify, request, current_app, g, abort

from app.api.auth import token_auth
from app.xapi import bp


@bp.route('/api/xapi', methods=['POST'])
@token_auth.login_required
def write_xapi():
    if g.current_user.role.role != 'admin':
        abort(403)
    data = request.get_json()
    user = g.current_user
    if user.role.role != 'admin' and user.role.role != 'system':
        abort(403)
    with open(current_app.config['FACT_STORE'], 'a+') as f:
        f.writelines([str(data) + '\n'])
    return jsonify(data)

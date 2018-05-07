# -*- coding: utf-8 -*-
"""
    xapi.routes
    ~~~~~~~~~~~

    Routes used for handeling xAPI data.
"""

from flask import jsonify, request, current_app

from app.api.auth import token_auth
from app.xapi import bp


@bp.route('/api/xapi', methods=['POST'])
@token_auth.login_required
def write_xapi():
    data = request.get_json()
    with open(current_app.config['FACT_STORE'], 'w+') as f:
        f.writelines([str(data)])
    return jsonify(data)

# -*- coding: utf-8 -*-
"""
    api.routes
    ~~~~~~~~~~

    The attendance API endpoints
"""
from flask import jsonify

from app.attendance import bp
from app.api.auth import token_auth
from app.api.errors import bad_request


@bp.route('/api/attendance/test')
@token_auth.login_required
def attendance_api_test():
    return jsonify({'test': 'attendance api test endpoint'})

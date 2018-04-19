# -*- coding: utf-8 -*-
"""
    attendance.routes
    ~~~~~~~~~~~~~~~~~

    Routes and API endpoints used for showing attendance.
"""
from flask import jsonify

from app.attendance import bp
from app.api.auth import token_auth


@bp.route('/api/attendance/<item_id>/', methods=['POST'])
@token_auth.login_required
def api_attend_lesson(item_id):
    return jsonify({'items': [item_id]})

# -*- coding: utf-8 -*-
"""
    attendance.routes
    ~~~~~~~~~~~~~~~~~

    Routes and API endpoints used for showing attendance.
"""
from flask import jsonify, url_for

from app.attendance import bp
from app.api.auth import token_auth
from app.models import Schedule




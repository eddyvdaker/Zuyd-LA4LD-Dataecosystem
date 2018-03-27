# -*- coding: utf-8 -*-
"""
    app.main.routes
    ~~~~~~~~~~~~~~~

    Routes for the data ecosystem
"""

from app.main import bp
from app import TDD_TEST_ENV


@bp.route('/')
def index():
    return f'<p>{TDD_TEST_ENV}</p>'

# -*- coding: utf-8 -*-
"""
    app.main.routes
    ~~~~~~~~~~~~~~~

    Routes for the data ecosystem
"""

from app import app


@app.route('/')
def index():
    return '<p>Hello</p>'

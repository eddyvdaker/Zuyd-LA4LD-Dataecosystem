# -*- coding: utf-8 -*-
"""
    app.routes
    ~~~~~~~~~~

    Routes for the data ecosystem
"""

from app import app


@app.route('/')
def index():
    return '<p>Hello</p>'

# -*- coding: utf-8 -*-
"""
    la4ld
    ~~~~~

    A learning analytics for learning design data ecosystem build using Flask.
"""

from app import app, db
from app.models import User


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}

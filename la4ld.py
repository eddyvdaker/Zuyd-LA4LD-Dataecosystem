# -*- coding: utf-8 -*-
"""
    la4ld
    ~~~~~

    A learning analytics for learning design data ecosystem build using Flask.
"""

from app import create_app, db
from app.models import User, Module, Role


app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Module': Module, 'Role': Role}

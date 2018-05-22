# -*- coding: utf-8 -*-
"""
    auth.decorator
    ~~~~~~~~~~~~~~

    A decorator for checking if user is admin.
"""
from functools import wraps
from flask import abort, g


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kw):
        if g.current_user.role.role == 'admin':
            return func(*args, **kw)
        else:
            abort(403)
    return wrapper

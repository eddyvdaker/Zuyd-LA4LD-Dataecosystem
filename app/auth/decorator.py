# -*- coding: utf-8 -*-
"""
    app.auth.decorator
    ~~~~~~~~~~~~~~~~~~

    Custom decorator for checking if a user is admin or not
"""
from functools import wraps
from flask import abort, g
from flask_login import current_user


def admin_required(func):
    """Checks if a user has te admin role or not, aborts with a 403 forbidden
    error if user is not admin
    """
    @wraps(func)
    def wrapper(*args, **kw):
        if not current_user.is_anonymous:
            if current_user.role.role == 'admin':
                return func(*args, **kw)
        else:
            if g.current_user.role.role == 'admin':
                return func(*args, **kw)

        abort(403)
    return wrapper

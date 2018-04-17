# -*- coding: utf-8 -*-
"""
    attendance.routes
    ~~~~~~~~~~~~~~~~~

    Routes used for showing attendance.
"""
from app.attendance import bp


@bp.route('/attendance/test')
def attendance_test():
    return 'test'

# -*- coding: utf-8 -*-
"""
    la4ld
    ~~~~~

    A learning analytics for learning design data ecosystem build using Flask.
"""

from app import create_app, db
from app.models import User, Grade, Module, Result, Role, Schedule, \
    ScheduleItem, Group, Attendance, ApiKey


app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Grade': Grade, 'Module': Module,
            'Result': Result, 'Role': Role, 'Schedule': Schedule,
            'ScheduleItem': ScheduleItem, 'Group': Group,
            'Attendance': Attendance, 'ApiKey': ApiKey}

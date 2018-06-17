# -*- coding: utf-8 -*-
"""
    la4ld
    ~~~~~

    A learning analytics data ecosystem infrastructure for learning design
    build using Flask.
"""

from app import create_app, db
from app.models import User, Grade, Module, Result, Role, Schedule, \
    ScheduleItem, Group, Attendance, ApiKey, Questionnaire, \
    QuestionnaireScale, QuestionResult


app = create_app()


@app.shell_context_processor
def make_shell_context():
    """Loads the database and models for interacting with the database from
    the Flask shell.
    """
    return {'db': db,
            'User': User,
            'Grade': Grade,
            'Module': Module,
            'Result': Result,
            'Role': Role,
            'Schedule': Schedule,
            'ScheduleItem': ScheduleItem,
            'Group': Group,
            'Attendance': Attendance,
            'ApiKey': ApiKey,
            'Questionnaire': Questionnaire,
            'QuestionnaireScale': QuestionnaireScale,
            'QuestionResult': QuestionResult
            }

# -*- coding: utf-8 -*-
"""
    forms
    ~~~~~

    Generic forms used in different parts of the application.
"""

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField

from app import app


class ImportForm(FlaskForm):
    file = FileField('File', validators=[
        FileRequired(),
        FileAllowed(app.config['ALLOWED_EXTENSIONS'],
                    'Incorrect format, JSON required!')
    ])
    submit = SubmitField('Import')

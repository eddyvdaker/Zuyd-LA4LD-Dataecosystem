# -*- coding: utf-8 -*-
"""
    main.forms
    ~~~~~~~~~~

    Forms that do not fit with any of the more specific blueprints or are
    core features of the application.
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

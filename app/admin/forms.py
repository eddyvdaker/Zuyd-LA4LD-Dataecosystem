# -*- coding: utf-8 -*-
"""
    admin.forms
    ~~~~~~~~~~~

    Forms that are used within the admin panel blueprint of the
    application.
"""
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField


class ImportForm(FlaskForm):
    file = FileField('File', validators=[
        FileRequired(),
        FileAllowed(['json'], 'Incorrect format, JSON required!')
    ])
    submit = SubmitField('Import')

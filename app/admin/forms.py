# -*- coding: utf-8 -*-
"""
    admin.forms
    ~~~~~~~~~~~

    Forms that are used within the admin panel blueprint of the
    application.
"""
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField, StringField, FieldList, DateField
from wtforms.validators import DataRequired, Email


class ImportForm(FlaskForm):
    file = FileField('File', validators=[
        FileRequired(),
        FileAllowed(['json'], 'Incorrect format, JSON required!')
    ])
    submit = SubmitField('Import')


class EditUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Save Changes')


class EditModuleForm(FlaskForm):
    code = StringField('Code', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    start = DateField('Start', validators=[DataRequired()])
    end = DateField('End', validators=[DataRequired()])
    faculty = StringField('Faculty', validators=[DataRequired()])
    submit = SubmitField('Save Changes')

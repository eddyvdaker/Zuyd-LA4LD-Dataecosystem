# -*- coding: utf-8 -*-
"""
    admin.forms
    ~~~~~~~~~~~

    Forms that are used within the admin panel blueprint of the
    application.
"""
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField, StringField, SelectField, DateField, \
    DateTimeField
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
    role = SelectField('Role', validators=[DataRequired()])
    card_number = StringField('Card Number', validators=[DataRequired()])
    submit = SubmitField('Save Changes')


class EditModuleForm(FlaskForm):
    code = StringField('Code', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    start = DateField('Start', validators=[DataRequired()])
    end = DateField('End', validators=[DataRequired()])
    faculty = StringField('Faculty', validators=[DataRequired()])
    submit = SubmitField('Save Changes')


class EditScheduleForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    module = SelectField('Module', validators=[DataRequired()], coerce=int)
    group = SelectField('Group', validators=[DataRequired()], coerce=int)
    submit = SubmitField('Save Changes')


class EditScheduleItemForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    start = DateTimeField('Start', validators=[DataRequired()])
    end = DateTimeField('End', validators=[DataRequired()])
    room = StringField('Room')
    submit = SubmitField('Save Changes')

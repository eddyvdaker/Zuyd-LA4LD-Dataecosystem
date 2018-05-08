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
    DateTimeField, BooleanField
from wtforms.validators import DataRequired, Email

from app.forms import MultiCheckboxField


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


class EditGroupForm(FlaskForm):
    code = StringField('Group', validators=[DataRequired()])
    active = BooleanField('Active')
    submit = SubmitField('Save Changes')


class ManageGroupMembershipForm(FlaskForm):
    action = SelectField(
        'Action', validators=[DataRequired()],
        choices=[('add', 'Add'), ('remove', 'Remove')])
    users_list = MultiCheckboxField('Users', validators=[])
    groups_list = MultiCheckboxField('Groups', validators=[])
    submit = SubmitField('Save Changes')


class ManageModuleMembershipForm(FlaskForm):
    action = SelectField(
        'Action', validators=[DataRequired()],
        choices=[('add', 'Add'), ('remove', 'Remove')])
    users_list = MultiCheckboxField('Users', validators=[])
    modules_list = MultiCheckboxField('Modules', validators=[])
    roles = SelectField('Role', validators=[DataRequired()])
    submit = SubmitField('Save Changes')
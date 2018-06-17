# -*- coding: utf-8 -*-
"""
    app.admin.forms
    ~~~~~~~~~~~~~~~

    Forms for admin panel
"""
from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField, StringField, SelectField, DateField, \
    DateTimeField, BooleanField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Email, Length

from app.forms import MultiCheckboxField


class ImportForm(FlaskForm):
    """Generic import form"""
    file = FileField(_l('File'), validators=[
        FileRequired(),
        FileAllowed(['json'], _l('Incorrect format, JSON required!'))
    ])
    submit = SubmitField(_l('Import'))


class EditUserForm(FlaskForm):
    """Edit/add user form"""
    username = StringField(_l('Username'), validators=[DataRequired()])
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    role = SelectField(_l('Role'), validators=[DataRequired()])
    card_number = StringField(_l('Card Number'), validators=[DataRequired()])
    submit = SubmitField(_l('Save Changes'))


class EditModuleForm(FlaskForm):
    """Edit/add module form"""
    code = StringField(_l('Code'), validators=[DataRequired()])
    name = StringField(_l('Name'), validators=[DataRequired()])
    description = StringField(_l('Description'), validators=[DataRequired()])
    start = DateField(_l('Start'), validators=[DataRequired()])
    end = DateField(_l('End'), validators=[DataRequired()])
    faculty = StringField(_l('Faculty'), validators=[DataRequired()])
    submit = SubmitField(_l('Save Changes'))


class EditScheduleForm(FlaskForm):
    """Edit/add schedule form"""
    description = StringField(_l('Description'), validators=[DataRequired()])
    module = SelectField(_l('Module'), validators=[DataRequired()], coerce=int)
    group = SelectField(_l('Group'), validators=[DataRequired()], coerce=int)
    submit = SubmitField(_l('Save Changes'))


class EditScheduleItemForm(FlaskForm):
    """Edit/add schedule item form"""
    title = StringField(_l('Title'), validators=[DataRequired()])
    description = StringField(_l('Description'), validators=[DataRequired()])
    start = DateTimeField(_l('Start'), validators=[DataRequired()])
    end = DateTimeField(_l('End'), validators=[DataRequired()])
    room = StringField(_l('Room'))
    submit = SubmitField(_l('Save Changes'))


class EditGroupForm(FlaskForm):
    """Edit/add group form"""
    code = StringField(_l('Group'), validators=[DataRequired()])
    active = BooleanField(_l('Active'))
    submit = SubmitField(_l('Save Changes'))


class ManageGroupMembershipForm(FlaskForm):
    """Manage group membership form"""
    action = SelectField(
        'Action', validators=[DataRequired()],
        choices=[('add', _l('Add')), ('remove', _l('Remove'))])
    users_list = MultiCheckboxField(_l('Users'), validators=[])
    groups_list = MultiCheckboxField(_l('Groups'), validators=[])
    submit = SubmitField(_l('Save Changes'))


class ManageModuleMembershipForm(FlaskForm):
    """Manage module membership form"""
    action = SelectField(
        'Action', validators=[DataRequired()],
        choices=[('add', _l('Add')), ('remove', _l('Remove'))])
    users_list = MultiCheckboxField(_l('Users'), validators=[])
    modules_list = MultiCheckboxField(_l('Modules'), validators=[])
    roles = SelectField(_l('Role'), validators=[DataRequired()])
    submit = SubmitField(_l('Save Changes'))


class AddApiKeyForm(FlaskForm):
    """Edit/add API Key form"""
    key = StringField(
        _l('Key'), validators=[DataRequired(), Length(min=12, max=512)]
    )
    description = TextAreaField(_l('Description'))
    submit = SubmitField(_l('Create Key'))


class ApiKeyDeleteConfirmationForm(FlaskForm):
    """Confirm API key deletion form"""
    confirm = BooleanField(
        _l('Confirm deletion (this action cannot be reverted)'),
        validators=[DataRequired()]
    )
    submit = SubmitField(_l('Confirm'))


class AddQuestionnaireForm(FlaskForm):
    """Add/edit questionnaire form"""
    id = IntegerField(
        _l('Questionnaire number'),
        validators=[DataRequired()]
    )
    name = StringField(_l('Name'), validators=[DataRequired()])
    description = TextAreaField(_l('Description'))
    questionnaire_type = StringField(_l('Type'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))


class AddScaleForm(FlaskForm):
    """Add/edit scale form"""
    id = IntegerField(_l('Scale Number'), validators=[DataRequired()])
    name = StringField(_l('Name'), validators=[DataRequired()])
    description = TextAreaField(_l('Description'))
    submit = SubmitField(_l('Submit'))


class AddQuestionForm(FlaskForm):
    """Add/edit question form"""
    id = IntegerField(_l('Question Number'), validators=[DataRequired()])
    question = StringField(_l('Question'), validators=[DataRequired()])
    reversed = BooleanField(_l('Reversed'))
    submit = SubmitField(_l('Submit'))


class QuestionnaireDeleteConfirmationField(FlaskForm):
    """Confirm questionnaire and connected results deletion form"""
    confirm = BooleanField(
        _l('Confirm deletion (this action cannot be reverted)'),
        validators=[DataRequired()]
    )
    confirm2 = BooleanField(
        _l('I understand that all question results form this questionnaire'
           'will be deleted as well.'),
        validators=[DataRequired()]
    )
    submit = SubmitField(_l('Confirm'))


class ScaleDeleteConfirmationField(FlaskForm):
    """Confirm scale and connected results deletion form"""
    confirm = BooleanField(
        _l('Confirm deletion (this action cannot be reverted)'),
        validators=[DataRequired()]
    )
    confirm2 = BooleanField(
        _l('I understand that all question results form this scale'
           'will be deleted as well.'),
        validators=[DataRequired()]
    )
    submit = SubmitField(_l('Confirm'))


class QuestionDeleteConfirmationField(FlaskForm):
    """Confirm question and connected results deletion form"""
    confirm = BooleanField(
        _l('Confirm deletion (this action cannot be reverted)'),
        validators=[DataRequired()]
    )
    confirm2 = BooleanField(
        _l('I understand that all question results form this question'
           'will be deleted as well.'),
        validators=[DataRequired()]
    )
    submit = SubmitField(_l('Confirm'))

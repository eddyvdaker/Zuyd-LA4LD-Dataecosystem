from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField, StringField, SelectField, DateField, \
    DateTimeField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email, Length

from app.forms import MultiCheckboxField


class ImportForm(FlaskForm):
    file = FileField(_l('File'), validators=[
        FileRequired(),
        FileAllowed(['json'], _l('Incorrect format, JSON required!'))
    ])
    submit = SubmitField(_l('Import'))


class EditUserForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    role = SelectField(_l('Role'), validators=[DataRequired()])
    card_number = StringField(_l('Card Number'), validators=[DataRequired()])
    submit = SubmitField(_l('Save Changes'))


class EditModuleForm(FlaskForm):
    code = StringField(_l('Code'), validators=[DataRequired()])
    name = StringField(_l('Name'), validators=[DataRequired()])
    description = StringField(_l('Description'), validators=[DataRequired()])
    start = DateField(_l('Start'), validators=[DataRequired()])
    end = DateField(_l('End'), validators=[DataRequired()])
    faculty = StringField(_l('Faculty'), validators=[DataRequired()])
    submit = SubmitField(_l('Save Changes'))


class EditScheduleForm(FlaskForm):
    description = StringField(_l('Description'), validators=[DataRequired()])
    module = SelectField(_l('Module'), validators=[DataRequired()], coerce=int)
    group = SelectField(_l('Group'), validators=[DataRequired()], coerce=int)
    submit = SubmitField(_l('Save Changes'))


class EditScheduleItemForm(FlaskForm):
    title = StringField(_l('Title'), validators=[DataRequired()])
    description = StringField(_l('Description'), validators=[DataRequired()])
    start = DateTimeField(_l('Start'), validators=[DataRequired()])
    end = DateTimeField(_l('End'), validators=[DataRequired()])
    room = StringField(_l('Room'))
    submit = SubmitField(_l('Save Changes'))


class EditGroupForm(FlaskForm):
    code = StringField(_l('Group'), validators=[DataRequired()])
    active = BooleanField(_l('Active'))
    submit = SubmitField(_l('Save Changes'))


class ManageGroupMembershipForm(FlaskForm):
    action = SelectField(
        'Action', validators=[DataRequired()],
        choices=[('add', _l('Add')), ('remove', _l('Remove'))])
    users_list = MultiCheckboxField(_l('Users'), validators=[])
    groups_list = MultiCheckboxField(_l('Groups'), validators=[])
    submit = SubmitField(_l('Save Changes'))


class ManageModuleMembershipForm(FlaskForm):
    action = SelectField(
        'Action', validators=[DataRequired()],
        choices=[('add', _l('Add')), ('remove', _l('Remove'))])
    users_list = MultiCheckboxField(_l('Users'), validators=[])
    modules_list = MultiCheckboxField(_l('Modules'), validators=[])
    roles = SelectField(_l('Role'), validators=[DataRequired()])
    submit = SubmitField(_l('Save Changes'))


class AddApiKeyForm(FlaskForm):
    key = StringField(
        _l('Key'), validators=[DataRequired(), Length(min=12, max=512)]
    )
    description = TextAreaField(_l('Description'))
    submit = SubmitField(_l('Create Key'))


class ApiKeyDeleteConfirmationForm(FlaskForm):
    confirm = BooleanField(
        _l('Confirm deletion (this action cannot be reverted)'),
        validators=[DataRequired()]
    )
    submit = SubmitField(_l('Confirm'))

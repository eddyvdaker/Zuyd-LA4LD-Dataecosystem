# -*- coding: utf-8 -*-
"""
    app.auth.forms
    ~~~~~~~~~~~~~~

    Forms for authentication functionality
"""
from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo


class LoginForm(FlaskForm):
    """Login form"""
    username = StringField(_l('Username'), validators=[DataRequired()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Remember Me'))
    submit = SubmitField(_l('Sign In'))


class ResetPasswordRequestForm(FlaskForm):
    """Reset password request form"""
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    submit = SubmitField(_l('Request Password Reset'))


class ResetPasswordForm(FlaskForm):
    """Reset password form"""
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _l('Repeat Password'), validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField(_l('Request Password Reset'))


class ChangePasswordForm(FlaskForm):
    """Change password form"""
    old_password = PasswordField(
        _l('Current Password'), validators=[DataRequired()]
    )
    new_password = PasswordField(
        _l('New Password'), validators=[DataRequired()]
    )
    new_password_2 = PasswordField(
        _l('Retype New Password'),
        validators=[DataRequired(), EqualTo('new_password')]
    )
    submit = SubmitField(_l('Change Password'))

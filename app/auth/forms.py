# -*- coding: utf-8 -*-
"""
    auth.forms
    ~~~~~~~~~~

    Forms for the authentication blueprint of the application.
"""
from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Current Password',
                                 validators=[DataRequired()])
    new_password = PasswordField('New Password',
                                 validators=[DataRequired()])
    new_password_2 = PasswordField('Retype New Password',
                                   validators=[
                                       DataRequired(),
                                       EqualTo('new_password')
                                   ])
    submit = SubmitField('Change Password')

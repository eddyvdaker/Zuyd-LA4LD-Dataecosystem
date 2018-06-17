# -*- coding: utf-8 -*-
"""
    app.auth.email
    ~~~~~~~~~~~~~~

    Email handling for the password reset process
"""
from flask import current_app, render_template

from app.email import send_mail


def send_password_reset_email(user):
    """Generate a jwt token and send password reset email"""
    token = user.get_reset_password_token()
    send_mail(
        '[LA4LD] Reset Your Password',
        sender=current_app.config['ADMINS'][0],
        recipients=[user.email],
        text_body=render_template(
            'email/reset_password.txt', user=user, token=token
        ),
        html_body=render_template(
            'email/reset_password.html', user=user, token=token
        )
    )

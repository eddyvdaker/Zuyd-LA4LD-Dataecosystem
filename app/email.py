# -*- coding: utf-8 -*-
"""
    errors
    ~~~~~~

    Error handling for the application.
"""

from flask import render_template
from flask_mail import Message
from app import app, mail


def send_mail(subject, sender, recipients, text_body, html_body):
    """
    A basic email framework.

    :param subject: <str> subject for the mail
    :param sender: <str> who send the mail
    :param recipients: <str> who the mail is send to
    :param text_body: <str> plaintext version of the mail
    :param html_body: <str> html version of the mail
    """

    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_mail('[LA4LD] Reset Your Password',
              sender=app.config['ADMINS'][0],
              recipients=[user.email],
              text_body=render_template('email/reset_password.txt',
                                        user=user, token=token),
              html_body=render_template('email/reset_password.html',
                                        user=user, token=token))

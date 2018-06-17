# -*- coding: utf-8 -*-
"""
    app.email
    ~~~~~~~~~

    Helper functions for sending emails.
"""

from flask import current_app, render_template
from flask_mail import Message
from threading import Thread
from app import mail


def send_async_email(app, msg):
    """Send email in a separate thread"""
    with app.app_context():
        mail.send(msg)


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
    # Used _get_current_object as a hack to remove all global
    # instances off app. It was not possible to use current_app
    # from flask because that is only a mapping to the app object
    # not the object itself.
    Thread(target=send_async_email,
           args=(current_app._get_current_object(), msg)).start()


def send_new_user_email(user):
    send_mail('[LA4LD] New Account',
              sender=current_app.config['ADMINS'][0],
              recipients=[user['email']],
              text_body=render_template('email/new_account.txt', user=user),
              html_body=render_template('email/new_account.html', user=user))

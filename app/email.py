# -*- coding: utf-8 -*-
"""
    errors
    ~~~~~~

    Error handling for the application.
"""

from flask_mail import Message
from app import mail


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

# -*- coding: utf-8 -*-
"""
    tests.unit_tests.test_errors
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Unit tests for the error handling
"""

from .base import UnitTest
from app.email import send_mail


class TestEmail(UnitTest):

    def test_sending_email(self):
        send_mail('test_email',
                  'abc@abc.abc',
                  ['zuyd.la4ld.dataecosystem@gmail.com'],
                  'This is a test mail',
                  '<h1>This</h1><p> is a test mail</p>')

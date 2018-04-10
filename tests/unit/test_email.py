# -*- coding: utf-8 -*-
"""
    tests.unit_tests.test_errors
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Unit tests for the error handling
"""

from tests.unit.base import UnitTest
from app.email import send_mail


class TestEmail(UnitTest):

    def test_sending_email(self):
        """Tests the sending of emails"""
        send_mail('test_email',
                  'zuyd.la4ld.dataecosystem@gmail.com',
                  ['zuyd.la4ld.dataecosystem@gmail.com'],
                  'This is a test mail',
                  '<h1>This</h1><p> is a test mail</p>')

# -*- coding: utf-8 -*-
"""
    tests.unit_tests.test_errors
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Unit tests for the error handling
"""

from .base import UnitTest, BASE_URL
import os


class TestErrorHandling(UnitTest):

    def test_404_page(self):
        """
        Searches for a non-existing page and checks if it returns
        a 404 error.
        """
        self.client.get(BASE_URL + '/kljty20y')
        self.assert_template_used('404.html')

    def test_500_page(self):
        """
        Goes to the error 500 test page and checks if it returns
        a 500 error.
        """
        self.client.get(BASE_URL + '/error/test_500')
        self.assert_template_used('500.html')


class TestLogging(UnitTest):

    def test_file_logging(self):
        """Checks if logging file exists and if it contains text."""
        self.assertTrue(os.path.exists('logs/la4ld.log'))

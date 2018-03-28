# -*- coding: utf-8 -*-
"""
    tests.unit_tests.test_errors
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Unit tests for the error handling
"""

from .base import UnitTest, BASE_URL


class TestErrorHandling(UnitTest):

    def test_404_page(self):
        self.client.get(BASE_URL + 'kljty20y')
        self.assert_template_used('404.html')

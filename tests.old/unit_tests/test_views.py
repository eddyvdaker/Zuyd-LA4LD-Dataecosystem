# -*- coding: utf-8 -*-
"""
    tests.unit_tests.test_views
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Unit tests for the views
"""

from .base import BASE_URL, UnitTest


class HomePageTest(UnitTest):

    def test_uses_login_template(self):
        """Tests if the login page uses the correct template."""
        self.client.get(BASE_URL + '/login')
        self.assert_template_used('login.html')
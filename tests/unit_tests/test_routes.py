# -*- coding: utf-8 -*-
"""
    tests.functional_tests.test_layout
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Functional tests for layout and pages.
"""

from .base import UnitTest

from app.main import routes


class RouteTest(UnitTest):

    def test_home_page(self):
        assert 'Hello' in routes.index()


# -*- coding: utf-8 -*-
"""
    tests.functional_tests.test_layout
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Functional tests for layout and pages.
"""

from .base import FunctionalTest


class LayoutTest(FunctionalTest):

    def test_home_page(self):
        # User goes to home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # User sees text 'Hello' on home page
        text = self.browser.find_element_by_tag_name('div').text
        self.assertIn('LA4LD', text)

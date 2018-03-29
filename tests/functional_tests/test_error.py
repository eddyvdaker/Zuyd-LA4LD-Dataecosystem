# -*- coding: utf-8 -*-
"""
    tests.functional_tests.test_error
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Functional tests for error handling
"""

from .base import FunctionalTest


class ErrorTest(FunctionalTest):

    def test_404_page(self):
        # User goes to non existing page
        self.browser.get(self.live_server_url + '/kdasljgg23')
        self.browser.set_window_size(1024, 768)

        # User gets an 404 File Not Found error page
        text = self.browser.find_element_by_tag_name('div').text
        self.assertIn('LA4LD', text)

        text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('File Not Found', text)

    def test_500_page(self):
        # User triggers a bug
        self.browser.get(self.live_server_url + '/error/test_500')
        self.browser.set_window_size(1024, 768)

        # User gets a 500 Internal Server Error page
        text = self.browser.find_element_by_tag_name('div').text
        self.assertIn('LA4LD', text)

        text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('An unexpected error has occurred', text)

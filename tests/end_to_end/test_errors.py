# -*- coding: utf-8 -*-
"""
    tests.end-to-end.test_errors
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    End-to-end tests for error handling
"""
from tests.end_to_end.base import EndToEndTest


class TestErrors(EndToEndTest):

    def test_403(self):
        pass
        # User logs in as student user
        self.loginUser('student', 'la4ld')

        # User tries to reach admin page
        self.browser.get(self.live_server_url + '/admin')

        # User gets 403 - Forbidden error
        text = self.waitFor(
            lambda: self.browser.find_element_by_tag_name('h1')
        ).text
        self.assertIn('403 - Forbidden', text)

        # User also sees back link
        back_link = self.waitFor(
            lambda: self.browser.find_elements_by_tag_name('a')
        )
        self.assertInList(
            self.live_server_url + '/',
            [x.get_attribute('href') for x in back_link]
        )

    def test_404(self):
        # User goes to non-existing page
        self.browser.get(self.live_server_url + '/209g0932gfhj294tg')

        # User gets an 404 File Not Found error page
        text = self.waitFor(
            lambda: self.browser.find_element_by_tag_name('h1').text
        )
        self.assertIn('404 - File Not Found', text)

        # User also sees back link
        back_link = self.waitFor(
            lambda: self.browser.find_elements_by_tag_name('a')
        )
        self.assertInList(
            self.live_server_url + '/',
            [x.get_attribute('href') for x in back_link]
        )

    def test_500(self):
        # User goes to the error test page
        self.browser.get(self.live_server_url + '/error/test_500')

        # User gets an 500 - Internal Server Error page
        text = self.waitFor(
            lambda: self.browser.find_element_by_tag_name('h1').text
        )
        self.assertIn('500 - Internal Server Error', text)

        # User also sees back link
        back_link = self.waitFor(
            lambda: self.browser.find_elements_by_tag_name('a')
        )
        self.assertInList(
            self.live_server_url + '/',
            [x.get_attribute('href') for x in back_link]
        )

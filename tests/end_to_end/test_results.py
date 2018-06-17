# -*- coding: utf-8 -*-
"""
    tests.end_to_end.test_results
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    End-to-end tests for results page
"""
from tests.end_to_end.base import EndToEndTest


class TestResults(EndToEndTest):

    def test_results_page(self):
        """Test if results page is available and contains correct data"""
        # User goes to login page and logs in
        self.loginUser(self.users['student'], 'la4ld')

        # User goes to results page and sees his own results
        self.browser.get(self.live_server_url + '/results')

        rows = self.waitFor(
            lambda: self.browser.find_elements_by_id('row')
        )

        rows_results = [
            x.find_elements_by_tag_name('td')[0].text for x in rows
        ]
        assert 'B2S1' in rows_results

# -*- coding: utf-8 -*-
"""
    tests.end_to_end.test_admin
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Tests for the administration panel
"""
import os

from tests.end_to_end.base import EndToEndTest


class TestAdmin(EndToEndTest):

    def test_admin_panel(self):
        """Test if admin panel is available"""
        # User goes to login page and logs in
        self.loginUser(self.users['admin'], 'la4ld')

        # User is an admin user and goes to the admin page
        self.browser.get(self.live_server_url + '/admin')

        text = self.waitFor(
            lambda: self.browser.find_element_by_tag_name('h1').text
        )
        self.assertIn('Admin Panel', text)

    def test_log_screen(self):
        """Test if logged out user going to admin panel is redirected to a
        login screen
        """
        # User goes to login page and logs in
        self.loginUser(self.users['admin'], 'la4ld')

        # User is admin and goes to the logs page
        self.browser.get(self.live_server_url + '/admin/logs')

        text = self.waitFor(
            lambda: self.browser.find_element_by_tag_name('h1').text
        )
        self.assertIn('Admin Panel: Logs', text)

        # User checks the logs and sees a startup event
        log_text = self.waitFor(
            lambda: self.browser.find_element_by_id('logs').text
        )
        self.assertIn('INFO: LA4LD - Startup [in', log_text)

        # User downloads the logs
        download_button = self.waitFor(
            lambda: self.browser.find_element_by_id('download-button')
        )
        download_button.click()
        assert os.path.exists('/tmp/la4ld.log')

        with open('/tmp/la4ld.log') as f:
            log_text_from_file = f.read()
        assert 'INFO: LA4LD - Startup [in' in log_text_from_file

        if os.path.exists('/tmp/la4ld.log'):
            os.remove('/tmp/la4ld.log')

    def test_user_overview(self):
        """Test if user overview screen is available"""
        # User goes to login page and logs in
        self.loginUser(self.users['admin'], 'la4ld')

        # User is admin and goes to user overview
        self.browser.get(self.live_server_url + '/admin/users_overview')

        rows = self.waitFor(
            lambda: self.browser.find_elements_by_id('row')
        )

        rows_username = [
            x.find_elements_by_tag_name('td')[1].text for x in rows
        ]
        assert self.users['student'] in rows_username

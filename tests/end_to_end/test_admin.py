import os
from time import sleep
from selenium.webdriver.common.keys import Keys

from tests.end_to_end.base import EndToEndTest


class TestAdmin(EndToEndTest):

    def test_admin_panel(self):
        # User goes to login page and logs in
        self.loginUser(self.users['admin'], 'la4ld')

        # User is an admin user and goes to the admin page
        self.browser.get(self.live_server_url + '/admin')

        text = self.waitFor(
            lambda: self.browser.find_element_by_tag_name('h1').text
        )
        self.assertIn('Admin Panel', text)

    def test_log_screen(self):
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

    # def test_adding_and_deleting_user(self):
    #     # User goes to login page and logs in
    #     self.loginUser(self.users['admin'], 'la4ld')
    #
    #     # User first checks if the user is not already in the system
    #     self.browser.get(self.live_server_url + '/admin/users_overview')
    #
    #     rows = self.waitFor(
    #         lambda: self.browser.find_elements_by_id('row')
    #     )
    #
    #     rows_username = [
    #         x.find_elements_by_tag_name('td')[1].text for x in rows
    #     ]
    #
    #     assert 'TESTUSER' not in rows_username
    #
    #     # User goes to add user page and is admin
    #     self.browser.get(self.live_server_url + '/admin/add_user')
    #
    #     username_input = self.browser.find_element_by_id('username')
    #     email_input = self.browser.find_element_by_id('email')
    #     card_input = self.browser.find_element_by_id('card_number')
    #     submit_input = self.browser.find_element_by_id('submit')
    #
    #     username_input.send_keys('TESTUSER')
    #     email_input.send_keys('TESTUSER@la4ld-test.com')
    #     card_input.send_keys(1234567890987654321)
    #     submit_input.send_keys(Keys.ENTER)
    #
    #     # User checks if the new user has been added
    #     self.browser.get(self.live_server_url + '/admin/users_overview')
    #
    #     rows = self.waitFor(
    #         lambda: self.browser.find_elements_by_id('row')
    #     )
    #
    #     rows_username = [
    #         x.find_elements_by_tag_name('td')[1].text for x in rows
    #     ]
    #
    #     assert 'TESTUSER' in rows_username

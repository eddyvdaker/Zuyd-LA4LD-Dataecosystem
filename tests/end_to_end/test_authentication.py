
# -*- coding: utf-8 -*-
"""
    tests.end-to-end.test_authentication
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    End-to-end tests for authentication
"""
from tests.end_to_end.base import EndToEndTest
from time import sleep


class TestAuthentication(EndToEndTest):

    def test_login(self):
        # User goes to login page
        self.browser.get(self.live_server_url + '/login')

        text = self.waitFor(
            lambda: self.browser.find_element_by_tag_name('h1').text
        )
        self.assertIn('Sign in', text)

        # User logs in
        self.loginUser(self.users['student'], 'la4ld')

        # User sees welcome message
        text = self.waitFor(
            lambda: self.browser.find_element_by_tag_name('h1').text
        )
        self.assertIn('Home', text)

        text = self.waitFor(
            lambda: self.browser.find_element_by_tag_name('p').text
        )
        self.assertIn(f'Hello, {self.users["student"]}', text)

    def test_wrong_username(self):
        # User goes to login page
        self.browser.get(self.live_server_url + '/login')

        text = self.waitFor(
            lambda: self.browser.find_element_by_tag_name('h1').text
        )
        self.assertIn('Sign in', text)

        # User logs in
        self.loginUser('alskdjfwoiefj', 'la4ld')
        text_list = self.waitFor(
            lambda: self.browser.find_element_by_id('messages')
        )
        text_items = text_list.find_elements_by_tag_name('li')
        self.assertInList(
            'Invalid username or password', [x.text for x in text_items]
        )

    def test_wrong_password(self):
        # User goes to login page
        self.browser.get(self.live_server_url + '/login')

        text = self.waitFor(
            lambda: self.browser.find_element_by_tag_name('h1').text
        )
        self.assertIn('Sign in', text)

        # User logs in
        self.loginUser(self.users['student'], 'j209fj0923g3290g')
        text_list = self.waitFor(
            lambda: self.browser.find_element_by_id('messages')
        )
        text_items = text_list.find_elements_by_tag_name('li')
        self.assertInList(
            'Invalid username or password', [x.text for x in text_items]
        )

    def test_logout(self):
        # User goes to login page
        self.browser.get(self.live_server_url + '/login')

        text = self.waitFor(
            lambda: self.browser.find_element_by_tag_name('h1').text
        )
        self.assertIn('Sign in', text)

        # User logs in
        self.loginUser(self.users['student'], 'la4ld')

        # User sees welcome message
        text = self.waitFor(
            lambda: self.browser.find_element_by_tag_name('h1').text
        )
        self.assertIn('Home', text)

        text = self.waitFor(
            lambda: self.browser.find_element_by_tag_name('p').text
        )
        self.assertIn(f'Hello, {self.users["student"]}', text)

        # User logs out
        self.browser.get(self.live_server_url + '/logout')

        # User is redirected to home page
        text = self.waitFor(
            lambda: self.browser.find_element_by_tag_name('p').text
        )
        self.assertIn('please log in', text)

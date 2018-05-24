from tests.end_to_end.base import EndToEndTest
from time import sleep


class TestProfile(EndToEndTest):

    def test_profile_page(self):
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

        # User goes to profile page
        self.browser.get(self.live_server_url + '/profile')

        text = self.waitFor(
            lambda: self.browser.find_element_by_tag_name('h1').text
        )
        self.assertIn('Profile', text)

        # Check if export button exists
        links_list = self.waitFor(
            lambda: self.browser.find_elements_by_tag_name('a')
        )
        self.assertInList(
            '/download/my-data', [x.get_attribute('href') for x in links_list]
        )

        account_details = self.waitFor(
            lambda: self.browser.find_elements_by_tag_name('strong')
        )
        account_details = [x.text for x in account_details]
        self.assertInList('Your role is:', account_details)
        self.assertInList('Your card number:', account_details)
        self.assertInList('Your identifier is:', account_details)

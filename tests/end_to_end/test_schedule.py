from tests.end_to_end.base import EndToEndTest


class TestSchedule(EndToEndTest):

    def test_schedule_selector(self):
        # User goes to login page and logs in
        self.loginUser(self.users['student'], 'la4ld')

        # User goes to the schedule selector page and sees his a drop down
        # menu
        self.browser.get(self.live_server_url + '/schedule')

        options = self.waitFor(
            lambda: self.browser.find_elements_by_tag_name('option')
        )
        options_text = [
            x.text for x in options
        ]
        assert 'ITS1-B2S1' in options_text

    def test_schedule_view(self):
        # User goes to login page and logs in
        self.loginUser(self.users['student'], 'la4ld')

        # User goes to the schedule 1 page and sees the selected schedule
        self.browser.get(self.live_server_url + '/schedule/1')

        rows = self.waitFor(
            lambda: self.browser.find_elements_by_id('row')
        )

        row_items = [
            x.find_elements_by_tag_name('td')[0].text for x in rows
        ]

        assert 'B2S1 Week 1 - les 1' in row_items

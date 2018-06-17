# -*- coding: utf-8 -*-
"""
    tests.unit.attendance
    ~~~~~~~~~~~~~~~~~~~~~

    End-to-end tests for attendance tracking
"""
from tests.end_to_end.base import EndToEndTest


class TestAttendance(EndToEndTest):

    def test_attendance(self):
        """Test if attendance page is available for student"""
        # User goes to login page and logs in
        self.loginUser(self.users['student'], 'la4ld')

        # User goes to the attendance page and sees his own results
        self.browser.get(self.live_server_url + '/attendance')

        rows = self.waitFor(
            lambda: self.browser.find_elements_by_id('row')
        )

        row_attendance = [
            x.find_elements_by_tag_name('td')[0].text for x in rows
        ]
        assert 'B2S1 Week 1 - les 1' in row_attendance

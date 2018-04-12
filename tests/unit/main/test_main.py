# -*- coding: utf-8 -*-
"""
    tests.unit.main.test_main
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Unit tests for the admin page
"""
from tests.unit.base import UnitTest


class TestIndexView(UnitTest):

    def test_index_route(self):
        """Test if the index/landing page is working"""
        resp = self.app.get('/')
        assert b'Home Page' in resp.data


class TestProfileView(UnitTest):

    def test_profile_route(self):
        """Test if the profile page is available for authenticated users"""
        with self.app.session_transaction() as sess:
            sess['user_id'] = 1
            sess['_fresh'] = True
        resp = self.app.get('/profile')
        assert b'Profile' in resp.data

    def test_profile_route_redirect(self):
        """
        Test if unauthenticated users get redirected when browsing to the
        profile page.
        """
        resp = self.app.get('/profile')
        assert resp.status_code == 302

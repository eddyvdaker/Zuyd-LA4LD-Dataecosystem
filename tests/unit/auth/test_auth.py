# -*- coding: utf-8 -*-
"""
    tests.unit.auth.test_auth
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Unit tests for user authentication
"""
from tests.unit.base import UnitTest


class TestLoginView(UnitTest):

    def test_login_route(self):
        """Test if login route is available"""
        resp = self.app.get('/login')
        assert b'login' in resp.data

    def test_login_route_redirect(self):
        """Test if unauthenticated user is redirected if not logged in"""
        resp = self.app.get('/profile')
        assert resp.status_code == 302

    def test_authenticated_user_redirected_from_login_route(self):
        """
        Test if logged in users are redirected to the index page
        from the login page
        """
        with self.app.session_transaction() as sess:
            sess['user_id'] = 1
            sess['_fresh'] = True
        resp = self.app.get('login')
        assert resp.status_code == 302

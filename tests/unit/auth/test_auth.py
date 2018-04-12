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


class TestChangingPassword(UnitTest):

    def test_change_password_route(self):
        """Tests if the change password route is available"""
        with self.app.session_transaction() as sess:
            sess['user_id'] = 1
            sess['_fresh'] = True
        resp = self.app.get('/change_password')
        assert b'Change Password' in resp.data

    def test_change_password_route_logged_out(self):
        """
        Tests if a logged out user is redirected to the login page for
        the change password route
        """
        resp = self.app.get('/change_password')
        assert resp.status_code == 302

    def test_changing_password(self):
        """Tests if changing password view post requests works"""
        with self.app.session_transaction() as sess:
            sess['user_id'] = 1
            sess['_fresh'] = True
        data = {'old_password': 'cat', 'new_password': 'dog',
                'new_password_2': 'dog', 'submit': 'Change Password'}
        resp = self.app.post('/change_password', data=data,
                             content_type='application/x-www-form-urlencoded')
        assert resp.status_code == 200


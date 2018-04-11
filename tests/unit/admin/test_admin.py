# -*- coding: utf-8 -*-
"""
    tests.unit.admin.test_admin
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Unit tests for the admin page
"""
from io import BytesIO

from tests.unit.base import UnitTest


class TestAdminView(UnitTest):

    def test_admin_route(self):
        """Test if the admin route works"""
        with self.app.session_transaction() as sess:
            sess['user_id'] = 1
            sess['_fresh'] = True
        resp = self.app.get('/admin')
        assert b'admin' in resp.data

    def test_admin_route_without_account(self):
        """Test if the admin route redirects to login page if not logged in"""
        resp = self.app.get('/admin', follow_redirects=True)
        assert b'login' in resp.data

    def test_admin_route_with_non_admin_account(self):
        """
        Test if the admin route throws a 403 error if not logged in with
        an admin account
        """
        with self.app.session_transaction() as sess:
            sess['user_id'] = 2
            sess['_fresh'] = True
        resp = self.app.get('/admin', follow_redirects=True)
        assert resp.status_code == 403


class TestAdminUpload(UnitTest):

    def generate_test_file(self, input, filename):
        """
        Gets input and filename and returns a dictionary where the file
        field represents an encoded file.

        :param input: <str> Content of the file
        :param filename: <str> Name of the file
        :return: Dict with encoded file in file field
        """

        """"""
        return {
            'field': 'value',
            'file': (BytesIO(str(input).encode('utf-8')), filename)
        }

    def test_file_upload(self):
        """Test if files uploaded can be found on the filesystem"""
        with self.app.session_transaction() as sess:
            sess['user_id'] = 1
            sess['_fresh'] = True

        data = self.generate_test_file({
            'users': [
                {
                    'username': 'test1',
                    'email': 'test1@la4ld.com',
                    'role': 'student'
                },
                {
                    'username': 'test2',
                    'email': 'test2@la4ld.com',
                    'role': 'admin'
                }
            ]
        }, 'test.json')

        resp = self.app.post('/admin', buffered=True,
                             content_type='multipart/form-data',
                             data=data)

        assert resp.status_code == 200

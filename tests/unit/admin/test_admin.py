# -*- coding: utf-8 -*-
"""
    tests.unit.admin_test_admin
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Unit tests for the admin page
"""
from flask import url_for

from app.admin.routes import admin
from tests.unit.base import ViewUnitTest


class TestAdminView(ViewUnitTest):

    def test_admin_template(self):
        response = self.client.get(url_for('admin.admin'),
                                   follow_redirects=True)
        self.assert_template_used('/admin/admin')

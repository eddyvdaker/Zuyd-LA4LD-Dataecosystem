# -*- coding: utf-8 -*-
"""
    tools.create_test_data
    ~~~~~~~~~~~~~~~~~~~~~~

    Create test data for use during development
"""

from app import db
from app.models import User, Role


roles = ['admin', 'student', 'teacher']

users = [
    {
        'username': 'student',
        'email': 'student@student.com',
        'role': 'student',
        'password': 'cat'
    },
    {
        'username': 'admin',
        'email': 'admin@admin.com',
        'role': 'admin',
        'password': 'cat'
    },
    {
        'username': 'teacher',
        'email': 'teacher@teacher.com',
        'role': 'teacher',
        'password': 'cat'
    }
]

for role in roles:
    r = Role(role=role)
    db.session.add(r)
db.session.commit()

for user in users:
    u = User(username=user['username'],
             email=user['email'])
    db.session.add(u)
    db.session.commit()

    r = Role.query.filter_by(role=user['role']).first()
    u.role_id = r.id
    db.session.commit()

    u = User.query.filter_by(username=user['username']).first()
    u.set_password(user['password'])
    db.session.commit()
db.session.commit()

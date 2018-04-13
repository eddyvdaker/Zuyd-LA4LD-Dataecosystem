# -*- coding: utf-8 -*-
"""
    tools.create_test_data
    ~~~~~~~~~~~~~~~~~~~~~~

    Create test data for use during development
"""
from datetime import datetime

from app import create_app, db
from app.models import User, Grade, Module, Result, Role

roles = ['admin', 'student', 'teacher']

users = [
    {
        'username': 'student',
        'email': 'student@la4ld-test.com',
        'role': 'student',
        'password': 'cat'
    },
    {
        'username': 'admin',
        'email': 'admin@la4ld-test.com',
        'role': 'admin',
        'password': 'cat'
    },
    {
        'username': 'teacher',
        'email': 'teacher@la4ld-test.com',
        'role': 'teacher',
        'password': 'cat'
    }
]

modules = [
    {
        'code': 'tm01',
        'name': 'Test Module 1',
        'description': 'The first testing module',
        'start': datetime(2010, 10, 1),
        'end': datetime(2010, 11, 1),
        'faculty': 'ICT'
    },
    {
        'code': 'tm02',
        'name': 'Test Module 2',
        'description': 'The second testing module',
        'start': datetime(2010, 10, 15),
        'end': datetime(2011, 3, 1),
        'faculty': 'Zorg'
    }
]


def create_roles():
    for role in roles:
        r = Role(role=role)
        db.session.add(r)
    db.session.commit()


def create_users():
    for user in users:
        u = User(
            username=user['username'],
            email=user['email']
        )
        db.session.add(u)
        db.session.commit()

        r = Role.query.filter_by(role=user['role']).first()
        u.role_id = r.id
        db.session.commit()

        u = User.query.filter_by(username=user['username']).first()
        u.set_password(user['password'])
        db.session.commit()
    db.session.commit()


def create_modules():
    for module in modules:
        m = Module(
            code=module['code'],
            name=module['name'],
            description=module['description'],
            start=module['start'],
            end=module['end'],
            faculty=module['faculty']
        )
        db.session.add(m)
    db.session.commit()


def add_users_to_modules():
    tm01 = Module.query.filter_by(code='tm01').first()
    tm02 = Module.query.filter_by(code='tm02').first()
    student = User.query.filter_by(username='student').first()
    teacher = User.query.filter_by(username='teacher').first()

    student.add_to_module(tm01)
    teacher.add_to_module(tm01, module_role='examiner')
    teacher.add_to_module(tm02, module_role='teacher')
    db.session.commit()


def add_results():
    student = User.query.filter_by(username='student').first()
    tm01 = Module.query.filter_by(code='tm01').first()

    r = Result(identifier=student.hash_identifier(), module=tm01.id)
    db.session.add(r)
    db.session.commit()

    g1 = Grade(name='pi1', score=6, weight=1, result=r.id)
    g2 = Grade(name='pi10', score=8, weight=4, result=r.id)
    db.session.add_all([g1, g2])
    db.session.commit()


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        create_roles()
        create_users()
        create_modules()
        add_users_to_modules()
        add_results()

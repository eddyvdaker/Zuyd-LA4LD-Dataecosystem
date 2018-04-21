# -*- coding: utf-8 -*-
"""
    models
    ~~~~~~

    The models for the data stored in the database.
"""
import base64
import hashlib
import jwt
import os
from datetime import datetime, timedelta
from flask import current_app, url_for
from flask_login import UserMixin
from time import time
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login

student_module = db.Table(
    'student_module',
    db.Column('student_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('module_id', db.Integer, db.ForeignKey('module.id'))
)

teacher_module = db.Table(
    'teacher_module',
    db.Column('teacher_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('module_id', db.Integer, db.ForeignKey('module.id'))
)

examiner_module = db.Table(
    'examiner_module',
    db.Column('examiner_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('module_id', db.Integer, db.ForeignKey('module.id'))
)

module_group = db.Table(
    'module_group',
    db.Column('module_id', db.Integer, db.ForeignKey('module.id')),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'))
)

student_group = db.Table(
    'student_group',
    db.Column('student_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'))
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    card_number = db.Column(db.String(128), index=True, unique=True)
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    module_as_student = db.relationship(
        'Module', secondary=student_module,
        primaryjoin=(student_module.c.student_id == id),
        backref=db.backref('student_id', lazy='dynamic'), lazy='dynamic'
    )
    module_as_teacher = db.relationship(
        'Module', secondary=teacher_module,
        primaryjoin=(teacher_module.c.teacher_id == id),
        backref=db.backref('teacher_id', lazy='dynamic'), lazy='dynamic'
    )
    module_as_examiner = db.relationship(
        'Module', secondary=examiner_module,
        primaryjoin=(examiner_module.c.examiner_id == id),
        backref=db.backref('examiner_id', lazy='dynamic'), lazy='dynamic'
    )
    groups = db.relationship(
        'Group', secondary=student_group,
        primaryjoin=(student_group.c.student_id == id),
        backref=db.backref('group_student_id', lazy='dynamic'),
        lazy='dynamic'
    )

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def add_to_module(self, module, module_role='student'):
        if module_role == 'student':
            if not self.student_of_module(module):
                self.module_as_student.append(module)
        if module_role == 'teacher':
            if not self.teacher_of_module(module):
                self.module_as_teacher.append(module)
        if module_role == 'examiner':
            if not self.examiner_of_module(module):
                self.module_as_examiner.append(module)

    def remove_from_module(self, module, module_role='student'):
        if module_role == 'student':
            if self.student_of_module(module):
                self.module_as_student.remove(module)
        if module_role == 'teacher':
            if self.teacher_of_module(module):
                self.module_as_teacher.remove(module)
        if module_role == 'examiner':
            if self.examiner_of_module(module):
                self.module_as_examiner.remove(module)

    def student_of_module(self, module):
        return self.module_as_student.filter(
            student_module.c.module_id == module.id).count() > 0

    def get_modules_of_student(self):
        return Module.query.join(
            student_module, (student_module.c.module_id == Module.id)).filter(
            student_module.c.student_id == self.id
        ).all()

    def teacher_of_module(self, module):
        return self.module_as_teacher.filter(
            teacher_module.c.module_id == module.id).count() > 0

    def get_modules_of_teacher(self):
        return Module.query.join(
            teacher_module, (teacher_module.c.module_id == Module.id)).filter(
            teacher_module.c.teacher_id == self.id
        ).all()

    def examiner_of_module(self, module):
        return self.module_as_examiner.filter(
            examiner_module.c.module_id == module.id).count() > 0

    def get_modules_of_examiner(self):
        return Module.query.join(
            examiner_module,
            (examiner_module.c.module_id == Module.id)).filter(
            examiner_module.c.examiner_id == self.id
        ).all()

    def add_to_group(self, group):
        if not self.student_in_group(group):
            self.groups.append(group)

    def remove_from_group(self, group):
        if self.student_in_group(group):
            self.groups.remove(group)

    def student_in_group(self, group):
        return self.groups.filter(
            student_group.c.group_id == group.id).count() > 0

    def groups_of_student(self):
        return Group.query.join(
            student_group,
            (student_group.c.group_id == Group.id)).filter(
            student_group.c.student_id == self.id
        ).all()

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(
                token, current_app.config['SECRET_KEY'],
                algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    def hash_identifier(self):
        return hashlib.sha512(str(
            self.username + current_app.config['HASH_KEY']).encode('utf-8')
        ).hexdigest()

    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(64), index=True, unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return f'<Role {self.role}>'


class Module(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(128), index=True)
    name = db.Column(db.String(128), index=True)
    description = db.Column(db.String(128))
    start = db.Column(db.DateTime)
    end = db.Column(db.DateTime)
    faculty = db.Column(db.String(128))
    students = db.relationship(
        'User', secondary=student_module,
        primaryjoin=(student_module.c.module_id == id),
        backref=db.backref('student_module_id', lazy='dynamic'),
        lazy='dynamic'
    )
    teachers = db.relationship(
        'User', secondary=teacher_module,
        primaryjoin=(teacher_module.c.module_id == id),
        backref=db.backref('teacher_module_id', lazy='dynamic'),
        lazy='dynamic'
    )
    examiners = db.relationship(
        'User', secondary=examiner_module,
        primaryjoin=(examiner_module.c.module_id == id),
        backref=db.backref('examiners_module_id', lazy='dynamic'),
        lazy='dynamic'
    )
    groups = db.relationship(
        'Group', secondary=module_group,
        primaryjoin=(module_group.c.module_id == id),
        backref=db.backref('group_module_id', lazy='dynamic'),
        lazy='dynamic'
    )
    results = db.relationship(
        'Result', backref='result_module', lazy='dynamic')

    def __repr__(self):
        return f'<Module {self.code}>'

    def get_students(self):
        return User.query.join(
            student_module, (student_module.c.student_id == User.id)).filter(
            student_module.c.module_id == self.id
        ).all()

    def get_teachers(self):
        return User.query.join(
            teacher_module, (teacher_module.c.teacger_id == User.id)).filter(
            teacher_module.c.module_id == self.id
        ).all()

    def get_examiners(self):
        return User.query.join(
            examiner_module,
            (examiner_module.c.examiner_id == User.id)).filter(
            examiner_module.c.module_id == self.id
        ).all()


class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    identifier = db.Column(db.String(128))
    module = db.Column(db.Integer, db.ForeignKey('module.id'))
    grades = db.relationship('Grade', backref='grade_result', lazy='dynamic')

    def __repr__(self):
        return f'<Result {self.id}>'


class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    score = db.Column(db.Float())
    weight = db.Column(db.Float())
    result = db.Column(db.String(128), db.ForeignKey('result.id'))


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(128))
    active = db.Column(db.Boolean)
    modules = db.relationship(
        'Module', secondary=module_group,
        primaryjoin=(module_group.c.group_id == id),
        backref=db.backref('module_group_id', lazy='dynamic'),
        lazy='dynamic'
    )
    students = db.relationship(
        'User', secondary=student_group,
        primaryjoin=(student_group.c.group_id == id),
        backref=db.backref('student_group_id', lazy='dynamic'),
        lazy='dynamic'
    )
    schedules = db.relationship(
        'Schedule', backref='group_schedule', lazy='dynamic')

    def module_in_group(self, module):
        return self.modules.filter(
            module_group.c.module_id == module.id).count() > 0

    def add_module_to_group(self, module):
        if not self.module_in_group(module):
            self.modules.append(module)

    def remove_module_from_group(self, module):
        if self.module_in_group(module):
            self.modules.remove(module)

    def get_modules_of_group(self):
        return Module.query.join(
            module_group, (module_group.c.module_id == Module.id)).filter(
            module_group.c.group_id == self.id
        ).all()


class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(256))
    group = db.Column(db.Integer, db.ForeignKey('group.id'))
    items = db.relationship(
        'ScheduleItem', backref='item_schedule', lazy='dynamic')

    def to_dict(self):
        data = {
            'id': self.id,
            'description': self.description,
            'group_id': self.group,
            '_links': {
                'self': url_for(
                    'schedule.api_single_schedule', schedule_id=self.id)
            }
        }
        return data


class ScheduleItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    description = db.Column(db.String(256))
    start = db.Column(db.DateTime)
    end = db.Column(db.DateTime)
    room = db.Column(db.String(128))
    schedule = db.Column(db.Integer, db.ForeignKey('schedule.id'))
    student_attendance = db.relationship(
        'Attendance', backref='item_attendance', lazy='dynamic')

    def to_dict(self):
        data = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'start': self.start,
            'end': self.end,
            'room': self.room
        }
        return data


class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    identifier = db.Column(db.String(128))
    schedule_item_id = db.Column(db.Integer, db.ForeignKey('schedule_item.id'))


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

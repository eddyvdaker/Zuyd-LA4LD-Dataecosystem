# -*- coding: utf-8 -*-
"""
    models
    ~~~~~~

    The models for the data stored in the database.
"""
from flask import current_app
from flask_login import UserMixin
import jwt
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


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
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
            examiner_module.c.module_id == Module.id).count() > 0

    def get_modules_of_examiner(self):
        return Module.query.join(
            examiner_module,
            (examiner_module.c.module_id == Module.id)).filter(
            examiner_module.c.examiner_id == self.id
        ).all()

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


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


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

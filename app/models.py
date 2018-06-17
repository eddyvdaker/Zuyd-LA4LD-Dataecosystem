# -*- coding: utf-8 -*-
"""
    app.models
    ~~~~~~~~~~

    The models for the data stored in the database.
"""
import base64
import hashlib
import jwt
import os
from datetime import datetime, timedelta
from flask import current_app
from flask_login import UserMixin
from time import time
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login

"""Student to module linking table"""
student_module = db.Table(
    'student_module',
    db.Column('student_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('module_id', db.Integer, db.ForeignKey('module.id'))
)

"""Teacher to module linking table"""
teacher_module = db.Table(
    'teacher_module',
    db.Column('teacher_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('module_id', db.Integer, db.ForeignKey('module.id'))
)

"""Examiner to module linking table"""
examiner_module = db.Table(
    'examiner_module',
    db.Column('examiner_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('module_id', db.Integer, db.ForeignKey('module.id'))
)

"""Module to group linking table"""
module_group = db.Table(
    'module_group',
    db.Column('module_id', db.Integer, db.ForeignKey('module.id')),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'))
)

"""Student to group linking table"""
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

    def to_dict(self, include_student_of=False, include_student_of_short=True,
                include_teacher_of=False, include_teacher_of_short=True,
                include_examiner_of=False, include_examiner_of_short=True,
                include_groups=False, include_groups_short=True):
        data = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'card_number': self.card_number,
            'role': self.role.role
        }

        if include_student_of:
            data['student_of'] = [
                x.to_dict for x in self.get_modules_of_student()
            ]
        elif include_student_of_short:
            data['student_of'] = [
                x.code for x in self.get_modules_of_student()
            ]

        if include_teacher_of:
            data['teacher_of'] = [
                x.to_dict() for x in self.get_modules_of_teacher()
            ]
        elif include_teacher_of_short:
            data['teacher_of'] = [
                x.code for x in self.get_modules_of_teacher()
            ]

        if include_examiner_of:
            data['examiner_of'] = [
                x.to_dict() for x in self.get_modules_of_examiner()
            ]
        elif include_examiner_of_short:
            data['examiner_of'] = [
                x.code for x in self.get_modules_of_examiner()
            ]

        if include_groups:
            data['groups'] = [x.to_dict() for x in self.groups_of_student()]
        elif include_groups_short:
            data['groups'] = [x.code for x in self.groups_of_student()]
        return data

    def set_password(self, password):
        """Set new password by hashing it and saving the hash in the db"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Hash password and check if it is the same as hash in the db"""
        return check_password_hash(self.password_hash, password)

    def add_to_module(self, module, module_role='student'):
        """Add user to module as specified role"""
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
        """Remove user from module as specified role"""
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
        """Check if user is student in a module"""
        return self.module_as_student.filter(
            student_module.c.module_id == module.id).count() > 0

    def get_modules_of_student(self):
        """Get all modules a user is student of"""
        return Module.query.join(
            student_module, (student_module.c.module_id == Module.id)).filter(
            student_module.c.student_id == self.id
        ).all()

    def teacher_of_module(self, module):
        """Check if user is teacher in a module"""
        return self.module_as_teacher.filter(
            teacher_module.c.module_id == module.id).count() > 0

    def get_modules_of_teacher(self):
        """Get all modules a user is teacher of"""
        return Module.query.join(
            teacher_module, (teacher_module.c.module_id == Module.id)).filter(
            teacher_module.c.teacher_id == self.id
        ).all()

    def examiner_of_module(self, module):
        """Check if user is examiner of module"""
        return self.module_as_examiner.filter(
            examiner_module.c.module_id == module.id).count() > 0

    def get_modules_of_examiner(self):
        """Get all modules user is examiner of"""
        return Module.query.join(
            examiner_module,
            (examiner_module.c.module_id == Module.id)).filter(
            examiner_module.c.examiner_id == self.id
        ).all()

    def add_to_group(self, group):
        """Add user to group"""
        if not self.student_in_group(group):
            self.groups.append(group)

    def remove_from_group(self, group):
        """Remove user from group"""
        if self.student_in_group(group):
            self.groups.remove(group)

    def student_in_group(self, group):
        """Check if user is in group"""
        return self.groups.filter(
            student_group.c.group_id == group.id).count() > 0

    def groups_of_student(self):
        """Get all groups user is a member of"""
        return Group.query.join(
            student_group,
            (student_group.c.group_id == Group.id)).filter(
            student_group.c.student_id == self.id
        ).all()

    def get_reset_password_token(self, expires_in=600):
        """Generate a jwt token for password reset"""
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        """Check if supplied jwt token is correct"""
        try:
            id = jwt.decode(
                token, current_app.config['SECRET_KEY'],
                algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    def hash_identifier(self):
        """Generate user identifier by hashing the users username + the hash
        key from the config file with SHA512
        """
        return hashlib.sha512(str(
            self.username + current_app.config['HASH_KEY']).encode('utf-8')
        ).hexdigest()

    def get_token(self, expires_in=3600):
        """Generate API token"""
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        """Revoke active API token"""
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        """Check if token is avaiable and whether it as expired (revoke if
        expired)
        """
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
        'Result', backref='result_module', lazy='dynamic'
    )

    def __repr__(self):
        return f'<Module {self.code}>'

    def to_dict(self, include_students=False, include_students_short=True,
                include_teachers=False, include_teachers_short=True,
                include_examiners=False, include_examiners_short=True,
                include_groups=False, include_groups_short=True,
                include_results=False):
        data = {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'description': self.description,
            'start': self.start.strftime('%Y-%m-%d'),
            'end': self.end.strftime('%Y-%m-%d'),
            'faculty': self.faculty
        }
        if include_students:
            data['students'] = [x.to_dict() for x in self.students.all()]
        elif include_students_short:
            data['students'] = [x.username for x in self.students.all()]

        if include_teachers:
            data['teachers'] = [x.to_dict() for x in self.teachers.all()]
        elif include_teachers_short:
            data['teachers'] = [x.username for x in self.teachers.all()]

        if include_examiners:
            data['examiners'] = [x.to_dict() for x in self.examiners.all()]
        elif include_examiners_short:
            data['examiners'] = [x.username for x in self.examiners.all()]

        if include_groups:
            data['groups'] = [x.to_dict() for x in self.groups.all()]
        elif include_groups_short:
            data['groups'] = [x.code for x in self.groups.all()]

        if include_results:
            data['results'] = [x.to_dict() for x in self.results.all()]

        return data

    def get_students(self):
        """Get students of module"""
        return User.query.join(
            student_module, (student_module.c.student_id == User.id)).filter(
            student_module.c.module_id == self.id
        ).all()

    def get_teachers(self):
        """Get teacher of module"""
        return User.query.join(
            teacher_module, (teacher_module.c.teacger_id == User.id)).filter(
            teacher_module.c.module_id == self.id
        ).all()

    def get_examiners(self):
        """Get examiners of module"""
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

    def to_dict(self, include_grades=True):
        data = {
            'id': self.id,
            'identifier': self.identifier,
            'module': self.result_module.code
        }
        if include_grades:
            data['grades'] = [x.to_dict() for x in self.grades.all()]
        return data


class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    score = db.Column(db.Float())
    weight = db.Column(db.Float())
    result = db.Column(db.String(128), db.ForeignKey('result.id'))

    def __repr__(self):
        return f'<Grade {self.id}>'

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'score': self.score,
            'weight': self.weight,
        }
        return data


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

    def __repr__(self):
        return f'<Group {self.id}>'

    def to_dict(self, include_modules=False, include_modules_short=True,
                include_students=False, include_students_short=True,
                include_schedules=False, include_schedules_short=True):
        data = {
            'id': self.id,
            'code': self.code,
            'active': self.active,
        }
        if include_modules:
            data['modules'] = [x.to_dict() for x in self.modules.all()]
        elif include_modules_short:
            data['modules'] = [x.code for x in self.modules.all()]

        if include_students:
            data['students'] = [x.to_dict() for x in self.students.all()]
        elif include_students_short:
            data['students'] = [x.username for x in self.students.all()]

        if include_schedules:
            data['schedules'] = [x.to_dict() for x in self.schedules.all()]
        elif include_schedules_short:
            data['schedules'] = [x.description for x in self.schedules.all()]

        return data

    def module_in_group(self, module):
        """Check if group is linked to a module"""
        return self.modules.filter(
            module_group.c.module_id == module.id).count() > 0

    def add_module_to_group(self, module):
        """Link group to module"""
        if not self.module_in_group(module):
            self.modules.append(module)

    def remove_module_from_group(self, module):
        """Remove link to module"""
        if self.module_in_group(module):
            self.modules.remove(module)

    def get_modules_of_group(self):
        """Get all modules this group is linked to"""
        return Module.query.join(
            module_group, (module_group.c.module_id == Module.id)).filter(
            module_group.c.group_id == self.id
        ).all()

    def get_students_of_group(self):
        """Get all members of group"""
        return User.query.join(
            student_group, (student_group.c.student_id == User.id)).filter(
            student_group.c.group_id == self.id
        ).all()


class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(256))
    group = db.Column(db.Integer, db.ForeignKey('group.id'))
    module = db.Column(db.Integer, db.ForeignKey('module.id'))
    items = db.relationship(
        'ScheduleItem', backref='item_schedule', lazy='dynamic')

    def __repr__(self):
        return f'<Schedule {self.id}>'

    def to_dict(self, include_items=True):
        data = {
            'id': self.id,
            'description': self.description,
            'group_id': self.group,
        }
        if include_items:
            data['items'] = [
                x.to_dict() for x in ScheduleItem.query.filter_by(
                    schedule=self.id
                )
            ]
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
        'Attendance', backref='item_attendance', lazy='dynamic'
    )

    def __repr__(self):
        return f'<ScheduleItem {self.id}>'

    def to_dict(self):
        data = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'start': self.start.strftime('%Y-%m-%d %H:%M'),
            'end': self.end.strftime('%Y-%m-%d %H:%M'),
            'room': self.room
        }
        return data

    def attended(self, user):
        """Check if a user with a certain identifier has attended this
        schedule item
        """
        attended = Attendance.query.filter_by(
            identifier=user.hash_identifier(),
            schedule_item_id=self.id
        ).first()
        return attended is not None


class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    identifier = db.Column(db.String(128))
    schedule_item_id = db.Column(db.Integer, db.ForeignKey('schedule_item.id'))

    def __repr__(self):
        return f'<Attendance {self.id}>'

    def to_dict(self):
        data = {
            'id': self.id,
            'identifier': self.identifier,
            'schedule_item': self.schedule_item_id
        }
        return data

    def get_schedule_item(self):
        """Get schedule item connected to this attendance record"""
        return ScheduleItem.query.filter_by(id=self.schedule_item_id).first()


class ApiKey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(1024), unique=True)
    description = db.Column(db.String(256))

    def __repr__(self):
        return f'<ApiKey {self.id}>'


class Questionnaire(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    questionnaire_id = db.Column(db.Integer)
    name = db.Column(db.String(64))
    description = db.Column(db.String(128))
    questionnaire_type = db.Column(db.String(64))
    questionnaire_scale = db.relationship(
        'QuestionnaireScale', backref='scale_questionnaire', lazy='dynamic'
    )

    def __repr__(self):
        return f'<Questionnaire {self.id}>'

    def to_dict(self, include_scales=True):
        data = {
            'id': self.id,
            'questionnaire_id': self.questionnaire_id,
            'identifier': self.identifier
        }

        if include_scales:
            data['scales'] = [
                x.to_dict() for x in self.questionnaire_scale.all()
            ]
        return data

    def get_questionnaire_for_user(self, user):
        """Get questionnaire including scales, questions and results for
        a user
        """
        data = {'questionnaire': self, 'scales': []}
        for scale in self.questionnaire_scale.all():
            scale_data = {'scale': scale, 'questions': [], 'score': 0.0}
            for question in scale.scale_questions.all():
                result = QuestionResult.query.filter_by(
                    question=question.id
                ).filter_by(
                    identifier=user.hash_identifier()
                ).first()
                scale_data['score'] += result.result
                scale_data['questions'].append({
                    'question': question, 'result': result
                })
            scale_data['score'] /= len(scale_data['questions'])
            data['scales'].append(scale_data)
        return data


class QuestionnaireScale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    scale = db.Column(db.Integer)
    name = db.Column(db.String(64))
    description = db.Column(db.String(128))
    questionnaire_id = db.Column(db.Integer, db.ForeignKey('questionnaire.id'))
    scale_questions = db.relationship(
        'Question', backref='question_scale', lazy='dynamic'
    )

    def __repr__(self):
        return f'<QuestionnaireScale {self.id}>'

    def to_dict(self, include_question_results=True):
        data = {
            'id': self.scale_id,
            'scale': self.scale,
            'name': self.name,
            'description': self.description,
            'questionnaire_id': self.questionnaire_id
        }

        if include_question_results:
            data['question_results'] = [
                x.to_dict() for x in self.question_results.all()
            ]
        return data


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_number = db.Column(db.Integer)
    question = db.Column(db.String(254))
    reversed = db.Column(db.Boolean)
    scale_id = db.Column(
        db.Integer, db.ForeignKey('questionnaire_scale.id')
    )
    question_results = db.relationship(
        'QuestionResult', backref='result_question', lazy='dynamic'
    )

    def __repr__(self):
        return f'<Question {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'number': self.question_number,
            'question': self.question,
            'reversed': self.reversed,
            'scale': self.scale_id
        }


class QuestionResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    identifier = db.Column(db.String(128))
    question = db.Column(db.Integer, db.ForeignKey('question.id'))
    result = db.Column(db.Float)
    date = db.Column(db.DateTime)

    def __repr__(self):
        return f'<QuestionResult {self.id}>'

    def to_dict(self, include_question=True, include_scale=True):
        data = {
            'id': self.id,
            'identifier': self.identifier,
            'result': db.Float,
        }

        if include_question:
            data['question'] = self.result_question.to_dict()
        else:
            data['question'] = self.question

        if include_scale:
            data['scale'] = self.result_question.question_scale.to_dict()
        return data


@login.user_loader
def load_user(id):
    """Specify which model is used to login (USER)"""
    return User.query.get(int(id))

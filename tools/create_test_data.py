# -*- coding: utf-8 -*-
"""
    tools.create_test_data
    ~~~~~~~~~~~~~~~~~~~~~~

    Create test data for use during development, testing or demonstrations.
    The data comes from the ./tools/test-data/test-data.json file, which is
    also a valid import file.
"""
import json
import os
from datetime import datetime
from random import randint, uniform

from app import db, create_app
from app.models import Role, Module, Group, Schedule, ScheduleItem, Result, \
    Attendance, User, Grade, Questionnaire, QuestionnaireScale, Question, \
    QuestionResult

basedir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(basedir, 'tools/test-data/test-data.json')) as f:
    test_data = json.load(f)


def create_roles():
    for role in ['admin', 'student', 'teacher']:
        r = Role(role=role)
        db.session.add(r)
    db.session.commit()


def create_modules(modules):
    for module in modules:
        m = Module(
            code=module['code'],
            name=module['name'],
            description=module['description'],
            start=datetime.strptime(module['start'], '%Y-%m-%d'),
            end=datetime.strptime(module['end'], '%Y-%m-%d'),
            faculty=module['faculty']
        )
        db.session.add(m)
        db.session.commit()


def create_groups(groups):
    for group in groups:
        grp = Group(
            code=group['code'],
            active=bool(group['active']),
        )
        db.session.add(grp)
        db.session.commit()
        for module in group['modules']:
            m = Module.query.filter_by(code=module).first()
            grp.add_module_to_group(m)
        db.session.commit()


def create_schedules(schedules):
    for schedule in schedules:
        s = Schedule(
            description=schedule['description'],
            group=Group.query.filter_by(code=schedule['group']).first().id,
            module=Module.query.filter_by(code=schedule['module']).first().id
        )
        db.session.add(s)
        db.session.commit()

        for item in schedule['items']:
            si = ScheduleItem(
                title=item['title'],
                description=item['description'],
                start=datetime.strptime(item['start'], '%Y-%m-%d %H:%M'),
                end=datetime.strptime(item['end'], '%Y-%m-%d %H:%M'),
                room=item['room'],
                schedule=s.id
            )
            db.session.add(si)
        db.session.commit()


def create_users(users):
    for user in users:
        print(user)
        # noinspection PyArgumentList
        u = User(
            username=user['username'],
            email=user['email'],
            role=Role.query.filter_by(role=user['role']).first(),
            card_number=user['cardnr']
        )
        db.session.add(u)
        db.session.commit()

        for group in user['groups']:
            u.add_to_group(Group.query.filter_by(code=group).first())

        for module in user['student_of']:
            u.add_to_module(
                Module.query.filter_by(code=module).first(), 'student'
            )

        for module in user['teacher_of']:
            u.add_to_module(
                Module.query.filter_by(code=module).first(), 'teacher'
            )

        for module in user['examiner_of']:
            u.add_to_module(
                Module.query.filter_by(code=module).first(), 'examiner'
            )

        u.set_password('la4ld')
        db.session.commit()


def create_admin():
    # noinspection PyArgumentList
    u = User(
        username='admin',
        email='admin@la4ld.com',
        role=Role.query.filter_by(role='admin').first()
    )
    u.set_password('la4ld')
    db.session.add(u)
    db.session.commit()


def generate_results(past_modules, pi_dicts):
    r = Role.query.filter_by(role='student').first()
    students = User.query.filter_by(role_id=r.id).all()

    for student in students:
        modules = [
            x for x in student.get_modules_of_student()
            if x.code in past_modules
        ]
        for module in modules:
            r = Result(
                identifier=student.hash_identifier(),
                module=module.id
            )
            db.session.add(r)
            db.session.commit()

            for pi in pi_dicts:
                grd = Grade(
                    name=pi['name'],
                    score=randint(0, 5) * 2,
                    weight=int(pi['weight']),
                    result=r.id
                )
                db.session.add(grd)
            db.session.commit()


def generate_attendance(rate=80):
    r = Role.query.filter_by(role='student').first()
    students = User.query.filter_by(role_id=r.id).all()

    for student in students:
        past_schedule_items = []
        for group in student.groups_of_student():
            for schedule in group.schedules.all():
                for x in schedule.items.all():
                    if x.end < datetime.now():
                        past_schedule_items.append(x)
        for item in past_schedule_items:
            if randint(1, 100) <= rate:
                a = Attendance(
                    identifier=student.hash_identifier(),
                    schedule_item_id=item.id
                )
                db.session.add(a)
                db.session.commit()


def create_questionnaire(mslq):
    q = Questionnaire(
        questionnaire_id=mslq['questionnaire_id'],
        name=mslq['name'],
        description=mslq['description'],
        questionnaire_type=mslq['questionnaire_type']
    )
    db.session.add(q)
    db.session.commit()

    for scale in mslq['scales']:
        qs = QuestionnaireScale(
            scale=scale['scale'],
            name=scale['name'],
            description=scale['description'],
        )
        db.session.add(qs)
        db.session.commit()

        for question in scale['questions']:
            sq = Question(
                question_number=question['number'],
                question=question['question'],
                reversed=question['reversed']
            )
            db.session.add(sq)
            db.session.commit()
            qs.scale_questions.append(sq)
            db.session.commit()
        q.questionnaire_scale.append(qs)
        db.session.commit()


def generate_mslq_results(mslq):
    r = Role.query.filter_by(role='student').first()
    students = User.query.filter_by(role_id=r.id).all()

    for student in students:
        for scale in mslq['scales']:
            for question in scale['questions']:
                qr = QuestionResult(
                    identifier=student.hash_identifier(),
                    question=Question.query.filter_by(
                        question_number=question['number']
                    ).first().id,
                    result=randint(1, 7)
                )
                db.session.add(qr)
                db.session.commit()


if __name__ == '__main__':
    user_input = input(
        'This script adds data to the application database, are you sure '
        'you want to continue? [y/N]: '
    )
    if user_input == 'y' or user_input == 'Y':
        app = create_app()
        app.config['TESTING'] = True
        with app.app_context():
            print('Creating modules...')
            create_modules(test_data['modules'])

            print('Creating groups...')
            create_groups(test_data['groups'])

            print('Creating roles...')
            create_roles()

            print('Creating users...')
            create_users(test_data['users'])

            print('Creating admin account...')
            create_admin()

            print('Creating schedules...')
            create_schedules(test_data['schedules'])

            print('Generating student results...')
            generate_results(
                ['B2S1', 'B2A1'],
                [
                    {'name': 'pi3', 'weight': 1},
                    {'name': 'pi4', 'weight': 2},
                    {'name': 'pi6', 'weight': 3},
                    {'name': 'pi9', 'weight': 5}
                ]
            )

            print('Generating student attendance...')
            generate_attendance()

            print('Creating MSLQ questionnaire...')
            create_questionnaire(test_data['mslq'])

            print('Generate MSLQ results...')
            generate_mslq_results(test_data['mslq'])

            print('Done...')

import json
import os
from datetime import datetime
from flask import current_app, flash, redirect, url_for
from flask_babel import _
from sqlalchemy.exc import IntegrityError
from secrets import token_urlsafe
from werkzeug.utils import secure_filename

from app import db
from app.email import send_new_user_email
from app.models import User, Grade, Module, Result, Role, Schedule, \
    ScheduleItem, Group, Questionnaire, QuestionResult, QuestionnaireScale, \
    Question


def upload_file(file):
    """
    Gets the file and filename from the form, makes sure it's secure, and
    saves it to the filesystem.

    :param file: <obj> file object containing the data
    :return: Path to file
    """
    f = file.data
    filename = secure_filename(f.filename)
    if not os.path.exists(current_app.config['IMPORT_FOLDER']):
        os.makedirs(current_app.config['IMPORT_FOLDER'])
    f.save(os.path.join(current_app.config['IMPORT_FOLDER'], filename))

    return os.path.join(current_app.config['IMPORT_FOLDER'], filename,)


def read_json(json_file, field=None):
    """
    Reads the imported json file.

    :param json_file: <str> The path to the json file
    :param field: <str> The field that is search for inside the
        json file, defaults to None
    :return: The json data read from the file
    """
    with open(json_file, 'r') as f:
        if field:
            try:
                data = json.load(f)[field]
            except KeyError:
                flash(_(f'Invalid file, missing key )' + field))
                return redirect(url_for('admin'))
        else:
            data = json.load(f)

    return data


def import_users_to_db(data, mail_details=False):
    """
    Writes the data from from the json file to the db

    :param data: <dict> Json data containing the user details
    :param mail_details: <bool> whether the users should receive a mail
        with their account credentials

    :return:
    """

    user_data = []
    users_skipped_data = []
    for row in data:
        try:
            # noinspection PyArgumentList
            user = User(
                username=row['username'], email=row['email'],
                card_number=row['cardnr']
            )
            db.session.add(user)
            db.session.commit()

            r = Role.query.filter_by(role=row['role']).first()
            user.role_id = r.id
            db.session.commit()

            # Generate random initial password for imported user
            password = token_urlsafe()
            user.set_password(password)
            db.session.commit()
            new_user = {
                'username': user.username,
                'password': password,
                'email': user.email,
                'cardnr': user.card_number
            }

            for group in row['groups']:
                user.add_to_group(Group.query.filter_by(
                    code=group).first())
            for module in row['student_of']:
                user.add_to_module(
                    Module.query.filter_by(code=module).first(),
                    module_role='student')
            for module in row['teacher_of']:
                user.add_to_module(
                    Module.query.filter_by(code=module).first(),
                    module_role='teacher')
            for module in row['examiner_of']:
                user.add_to_module(
                    Module.query.filter_by(code=module).first(),
                    module_role='examiner')

            db.session.commit()

            if mail_details:
                if 'la4ld-test.com' not in user.email:
                    send_new_user_email(new_user)
            else:
                user_data.append(new_user)
        except IntegrityError or KeyError:
            db.session.rollback()
            users_skipped_data.append(row['username'])

    return user_data, users_skipped_data


def import_modules_to_db(data):
    """
    Writes the module data from the json file to the db.

    :param data: <dict> Dictionary containing the module data
    :return: Number of imported modules
    """
    for row in data:
        try:
            module = Module(
                code=row['code'],
                name=row['name'],
                description=row['description'],
                start=datetime.strptime(row['start'], '%Y-%m-%d'),
                end=datetime.strptime(row['end'], '%Y-%m-%d'),
                faculty=row['faculty']
            )
            db.session.add(module)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

    return str(len(data))


def import_results_to_db(data):
    """
    Writes the results data from the json file to the db

    :param data: <dict> Dictionary containing results data
    :return: Number of imported results
    """
    for row in data:
        user = User.query.filter_by(username=row['username']).first()
        module = Module.query.filter_by(code='tm01').order_by(
            Module.start.desc()).first()
        r = Result(identifier=user.hash_identifier(), module=module.id)
        db.session.add(r)
        db.session.commit()

        for grade in row['grades']:
            g = Grade(name=grade['name'], score=grade['score'],
                      weight=grade['weight'], result=r.id)
            db.session.add(g)
            db.session.commit()

    return str(len(data))


def import_schedules_to_db(data):
    """
    Writes the schedule data from the json file to the db

    :param data: <dict> Dictionary containing schedule data
    :return: Number of imported schedules
    """
    for row in data:
        s = Schedule(description=row['description'])
        grp = Group.query.filter_by(code=row['group']).first()
        s.group = grp.id
        module = Module.query.filter_by(code=row['module']).first()
        s.module = module.id
        db.session.add(s)
        db.session.commit()

        for item in row['items']:
            si = ScheduleItem(
                title=item['title'],
                description=item['description'],
                start=datetime.strptime(item['start'], '%Y-%m-%d %H:%M'),
                end=datetime.strptime(item['end'], '%Y-%m-%d %H:%M'),
                room=item['room'],
                schedule=s.id)
            db.session.add(si)
            db.session.commit()
    return str(len(data))


def import_groups_to_db(data):
    """
    Writes the group data from the json file to the db

    :param data: <dict> Dictionary containing group data
    :return: Number of imported groups
    """
    for row in data:
        grp = Group(code=row['code'], active=row['active'])
        db.session.add(grp)
        db.session.commit()

        for module in row['modules']:
            grp.add_module_to_group(
                Module.query.filter_by(code=module).first())
        db.session.commit()
    return str(len(data))


def import_questionnaires_to_db(data):
    """
    Writes the MSLQ data from the json file to the db

    :param data:
    :return:
    """
    for row in data:
        q = Questionnaire.query.filter_by(
            questionnaire_id=row['questionnaire_id']
        ).first()
        if not q:
            q = Questionnaire(
                questionnaire_id=row['questionnaire_id'],
                name=f'imported-questionnaire-{row["questionnaire_id"]}',
                questionnaire_type=row['type']
            )
            db.session.add(q)
            db.session.commit()
        for scale in row['scales']:
            qs = QuestionnaireScale.query.filter_by(
                scale=scale['scale_id']
            ).first()
            if not qs:
                qs = QuestionnaireScale(
                    scale=scale['scale_id'],
                    name=scale['scale_name'],

                )
                db.session.add(qs)
                db.session.commit()
                q.questionnaire_scale.append(qs)
                db.session.commit()
            for question in scale['questions']:
                sq = Question.query.filter_by(
                    question_number=question['question_id']
                ).first()
                if not sq:
                    sq = Question(
                        question_number=question['question_id'],
                        reversed=question['reversed']
                    )
                    db.session.add(sq)
                    db.session.commit()
                    qs.scale_questions.append(sq)
                qr = QuestionResult(
                    identifier=row['student_identifier'],
                    result=question['result'],
                    date=datetime.strptime(scale['date'], '%Y-%m-%d %H:%M:%S')
                )
                db.session.add(qr)
                db.session.commit()
                sq.question_results.append(qr)
                db.session.commit()
    return str(len(data))

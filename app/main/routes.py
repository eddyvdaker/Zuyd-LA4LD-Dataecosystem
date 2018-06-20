# -*- coding: utf-8 -*-
"""
    app.main.routes
    ~~~~~~~~~~~~~~~

    Routes for main functionality
"""
import json
import os
from flask import abort, current_app, render_template, send_from_directory, \
    send_file
from flask_babel import _
from flask_login import current_user, login_required
from secrets import token_urlsafe

from app.main import bp
from app.models import Result, Attendance, ScheduleItem, Schedule, \
    QuestionResult
from app.auth.decorator import admin_required


def get_user_questionnaires(user_identifier):
    """Returns the questionnaires which has results for the user"""
    user_questions = QuestionResult.query.filter_by(
        identifier=user_identifier
    ).all()
    user_questionnaires = []
    for question in user_questions:
        q = question.result_question.question_scale.scale_questionnaire
        if q not in user_questionnaires:
            user_questionnaires.append(q)
    return user_questionnaires


def collect_schedule_data(user_identifier):
    """Get schedule data for user"""
    group_ids = [x.id for x in current_user.groups_of_student()]
    schedules = []
    for group_id in group_ids:
        for schedule in Schedule.query.filter_by(id=group_id):
            schedules.append(schedule)

    schedules_data = []

    for schedule in schedules:
        schedule_data = {
            'id': schedule.id,
            'description': schedule.description,
            'groups': schedule.group,
            'items': []
        }

        schedule_items = ScheduleItem.query.filter_by(schedule=schedule.id)
        for item in schedule_items:
            item_data = {
                    'id': item.id,
                    'title': item.title,
                    'description': item.description,
                    'start': item.start.strftime('%Y-%m-%d %H:%M'),
                    'end': item.end.strftime('%Y-%m-%d %H:%M'),
                    'room': item.room,
            }
            attended = Attendance.query.filter_by(
                identifier=user_identifier, schedule_item_id=item.id).all()
            if attended:
                item_data['attended'] = 'True'
            else:
                item_data['attended'] = 'False'
            schedule_data['items'].append(item_data)
        schedules_data.append(schedule_data)
    return schedules_data


@bp.route('/')
def index():
    """Home page"""
    return render_template('index.html', title=_('Home Page'))


@bp.route('/error/test_500')
def error_test_500():
    """Test page for testing 500 errors"""
    abort(500)


@bp.route('/profile')
@login_required
def profile():
    """Profile page for user"""
    modules_as_student = current_user.get_modules_of_student()
    modules_as_teacher = current_user.get_modules_of_teacher()
    modules_as_examiner = current_user.get_modules_of_examiner()

    return render_template(
        'profile.html', title=_('Profile'),
        modules_as_student=modules_as_student,
        modules_as_teacher=modules_as_teacher,
        modules_as_examiner=modules_as_examiner
    )


@bp.route('/uploads/<filename>')
@login_required
@admin_required
def uploaded_file(filename):
    """Generic upload file page"""
    return send_from_directory(current_app.config['IMPORT_FOLDER'], filename)


@bp.route('/download/my-data')
@login_required
def download_own_data():
    """Retrieve and download user data"""
    user_identifier = current_user.hash_identifier()
    user_results = Result.query.filter_by(identifier=user_identifier).all()

    user_data = {
        'user': current_user.to_dict(
            include_student_of=True,
            include_teacher_of=True,
            include_examiner_of=True,
            include_groups=True
        ),
        'results': [x.to_dict() for x in user_results],
        'schedules': collect_schedule_data(user_identifier),
        'questionnaires': [
            x.get_questionnaire_for_user(current_user)
            for x in get_user_questionnaires(user_identifier)
        ]
    }
    print(user_data)
    file_path = f'{current_app.config["EXPORT_FOLDER"]}{token_urlsafe(6)}'
    if not os.path.exists(current_app.config["EXPORT_FOLDER"]):
        os.makedirs(current_app.config["EXPORT_FOLDER"])
    with open(file_path, 'w+') as file:
        json.dump(user_data, file, indent=4)
    return send_file(
        file_path,
        mimetype='application/json',
        attachment_filename='my-data.json',
        as_attachment=True,
        cache_timeout=-1
    )

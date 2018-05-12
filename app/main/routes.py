# -*- coding: utf-8 -*-
"""
    main.routes
    ~~~~~~~~~~~

    Routes that do not fit with any of the more specific blueprints or are
    core features of the application.
"""
import json
import os
from flask import abort, current_app, render_template, send_from_directory, \
    send_file
from flask_babel import _
from flask_login import current_user, login_required
from secrets import token_urlsafe

from app.main import bp
from app.models import Result, Attendance, ScheduleItem, Schedule


def get_modules_data_for_role(modules):
    role_data = []
    for module in modules:
        role_data.append(
            {
                'id': module.id,
                'code': module.code,
                'name': module.name,
                'description': module.description,
                'start': module.start.strftime('%Y-%m-%d'),
                'end': module.end.strftime('%Y-%m-%d'),
                'faculty': module.faculty
            },
        )
    return role_data


def get_group_data_for_student():
    group_data = []
    for group in current_user.groups_of_student():
        group_data.append(
            {
                'id': group.id,
                'code': group.code,
                'active': group.active,
                'modules': [x.id for x in group.get_modules_of_group()]
            }
        )
    return group_data


def collect_user_data():
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "card_number": current_user.card_number,
        "role": current_user.role.role,
        'modules_as_student': get_modules_data_for_role(
            current_user.get_modules_of_student()),
        'modules_as_teacher': get_modules_data_for_role(
            current_user.get_modules_of_teacher()),
        'modules_as_examiner': get_modules_data_for_role(
            current_user.get_modules_of_examiner()),
        'groups': get_group_data_for_student()
    }


def collect_results_data(user_identifier):
    results = Result.query.filter_by(identifier=user_identifier)
    results_data = []
    for result in results:
        result_data = {'id': result.id, 'module': result.module}
        grades = result.grades.all()
        grades_data = []
        for grade in grades:
            grades_data.append(
                {
                    'name': grade.name,
                    'score': grade.score,
                    'weight': grade.weight
                }
            )
        result_data['grades'] = grades_data
        results_data.append(result_data)
    return results_data


def collect_schedule_data(user_identifier):
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
    return render_template('index.html', title=_('Home Page'))


@bp.route('/error/test_500')
def error_test_500():
    abort(500)


@bp.route('/profile')
@login_required
def profile():
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
def uploaded_file(filename):
    if current_user.role.role != 'admin':
        abort(403)
    return send_from_directory(current_app.config['IMPORT_FOLDER'], filename)


@bp.route('/download/my-data')
@login_required
def download_own_data():
    user_identifier = current_user.hash_identifier()
    user_data = {
        'user': collect_user_data(),
        'results': collect_results_data(user_identifier),
        'schedules': collect_schedule_data(user_identifier),
        'mslq': 'PLACEHOLDER'
    }
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

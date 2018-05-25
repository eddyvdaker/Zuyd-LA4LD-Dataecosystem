# -*- coding: utf-8 -*-
"""
    api.get_data
    ~~~~~~~~~~~~

    API endpoints for requesting data.
"""
from flask import jsonify

from app.models import User, Module, Result, Group, Schedule, Attendance, \
    Questionnaire
from app.api import bp
from app.api.auth import token_auth
from app.auth.decorator import admin_required


@bp.route('/api/data/users', methods=['GET'])
@token_auth.login_required
@admin_required
def get_users():
    return jsonify({'users': [x.to_dict() for x in User.query.all()]})


@bp.route('/api/data/user/<int:id>', methods=['GET'])
@token_auth.login_required
@admin_required
def get_user(id):
    return jsonify(User.query.filter_by(id=id).first_or_404().to_dict())


@bp.route('/api/data/modules', methods=['GET'])
@token_auth.login_required
def get_methods():
    return jsonify({'modules': [x.to_dict() for x in Module.query.all()]})


@bp.route('/api/data/module/<int:id>', methods=['GET'])
@token_auth.login_required
def get_method(id):
    return jsonify(Module.query.filter_by(id=id).first_or_404().to_dict())


@bp.route('/api/data/results', methods=['GET'])
@token_auth.login_required
@admin_required
def get_results():
    return jsonify({'results': [x.to_dict() for x in Result.query.all()]})


@bp.route('/api/data/result/<int:id>', methods=['GET'])
@token_auth.login_required
@admin_required
def get_result(id):
    return jsonify(Result.query.filter_by(id=id).first_or_404().to_dict())


@bp.route('/api/data/groups', methods=['GET'])
@token_auth.login_required
def get_groups():
    return jsonify({'groups': [x.to_dict() for x in Group.query.all()]})


@bp.route('/api/data/group/<int:id>', methods=['GET'])
@token_auth.login_required
def get_group(id):
    return jsonify(Group.query.filter_by(id=id).first_or_404().to_dict())


@bp.route('/api/data/schedules', methods=['GET'])
@token_auth.login_required
def get_schedules():
    return jsonify({'schedules': [x.to_dict() for x in Schedule.query.all()]})


@bp.route('/api/data/schedule/<int:id>', methods=['GET'])
@token_auth.login_required
def get_schedule(id):
    return jsonify(Schedule.query.filter_by(id=id).first_or_404().to_dict())


@bp.route('/api/data/attendance', methods=['GET'])
@token_auth.login_required
@admin_required
def get_attendance():
    return jsonify({
        'attendance': [x.to_dict() for x in Attendance.query.all()]
    })


@bp.route('/api/data/questionnaires', methods=['GET'])
@token_auth.login_required
@admin_required
def get_questionnaires():
    return jsonify({
        'questionnaires': [x.to_dict() for x in Questionnaire.query.all()]
    })

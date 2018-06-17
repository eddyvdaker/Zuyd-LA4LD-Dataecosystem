# -*- coding: utf-8 -*-
"""
    app.api.get_data
    ~~~~~~~~~~~~~~~~

    API calls for retrieving data
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
    """Get a list of users"""
    return jsonify({'users': [x.to_dict() for x in User.query.all()]})


@bp.route('/api/data/user/<int:id>', methods=['GET'])
@token_auth.login_required
@admin_required
def get_user(id):
    """Get specified user"""
    return jsonify(User.query.filter_by(id=id).first_or_404().to_dict())


@bp.route('/api/data/modules', methods=['GET'])
@token_auth.login_required
def get_modules():
    """Get a list of modules"""
    return jsonify({'modules': [x.to_dict() for x in Module.query.all()]})


@bp.route('/api/data/module/<int:id>', methods=['GET'])
@token_auth.login_required
def get_module(id):
    """Get a specified module"""
    return jsonify(Module.query.filter_by(id=id).first_or_404().to_dict())


@bp.route('/api/data/results', methods=['GET'])
@token_auth.login_required
@admin_required
def get_results():
    """Get a list of results"""
    return jsonify({'results': [x.to_dict() for x in Result.query.all()]})


@bp.route('/api/data/result/<int:id>', methods=['GET'])
@token_auth.login_required
@admin_required
def get_result(id):
    """Get a specific result"""
    return jsonify(Result.query.filter_by(id=id).first_or_404().to_dict())


@bp.route('/api/data/groups', methods=['GET'])
@token_auth.login_required
def get_groups():
    """Get a list of groups"""
    return jsonify({'groups': [x.to_dict() for x in Group.query.all()]})


@bp.route('/api/data/group/<int:id>', methods=['GET'])
@token_auth.login_required
def get_group(id):
    """Get a specific group"""
    return jsonify(Group.query.filter_by(id=id).first_or_404().to_dict())


@bp.route('/api/data/schedules', methods=['GET'])
@token_auth.login_required
def get_schedules():
    """Get a list of schedules"""
    return jsonify({'schedules': [x.to_dict() for x in Schedule.query.all()]})


@bp.route('/api/data/schedule/<int:id>', methods=['GET'])
@token_auth.login_required
def get_schedule(id):
    """Get a specific schedule"""
    return jsonify(Schedule.query.filter_by(id=id).first_or_404().to_dict())


@bp.route('/api/data/attendance', methods=['GET'])
@token_auth.login_required
@admin_required
def get_attendance():
    """Get a list of attendance results"""
    return jsonify({
        'attendance': [x.to_dict() for x in Attendance.query.all()]
    })


@bp.route('/api/data/questionnaires', methods=['GET'])
@token_auth.login_required
@admin_required
def get_questionnaires():
    """Get a list of questionnaires"""
    return jsonify({
        'questionnaires': [x.to_dict() for x in Questionnaire.query.all()]
    })

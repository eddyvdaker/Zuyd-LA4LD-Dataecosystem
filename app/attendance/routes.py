# -*- coding: utf-8 -*-
"""
    attendance.routes
    ~~~~~~~~~~~~~~~~~

    Routes and API endpoints used for showing attendance.
"""
from flask import jsonify, request, render_template, g, abort
from flask_babel import _
from flask_login import current_user, login_required

from app import db
from app.attendance import bp
from app.api.auth import token_auth
from app.auth.decorator import admin_required
from app.models import User, ScheduleItem, Attendance


@bp.route('/api/attendance/<item_id>', methods=['POST'])
@token_auth.login_required
@admin_required
def api_attend_lesson(item_id):
    data = request.get_json()
    student = User.query.filter_by(card_number=data['cardnr']).first()
    item = ScheduleItem.query.filter_by(id=item_id).first()

    attended = Attendance(
        identifier=student.hash_identifier(), schedule_item_id=item.id)
    db.session.add(attended)
    db.session.commit()

    return jsonify({'student': student.id, 'attended_schedule_item': item.id})


@bp.route('/attendance', methods=['GET'])
@login_required
def attendance():
    attended = Attendance.query.filter_by(
        identifier=current_user.hash_identifier()).all()

    return render_template(
        'attendance/attendance.html', attended=attended, title=_('Attendance')
    )

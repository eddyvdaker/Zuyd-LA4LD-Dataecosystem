# -*- coding: utf-8 -*-
"""
    app.schedule.routes
    ~~~~~~~~~~~~~~~~~~~

    Routes for schedules functionality
"""
from datetime import datetime, timedelta
from flask import jsonify, redirect, render_template, url_for
from flask_login import current_user
from flask_babel import _

from app.api.auth import token_auth
from app.models import Module, Schedule, ScheduleItem, Group
from app.schedule import bp
from app.schedule.forms import SelectSchedule


@bp.route('/schedule', methods=['GET', 'POST'])
def schedule():
    """Schedule selection page"""
    form = SelectSchedule()
    schedules = Schedule.query.all()
    choices = []
    for schedule in schedules:
        if schedule.group in [x.id for x in current_user.groups_of_student()]:
            choices.append((
                schedule.description,
                f'{schedule.description} (Your schedule)'
            ))
        else:
            choices.append((schedule.description, schedule.description))

    form.schedule.choices = choices
    if form.validate_on_submit():
        schedule_id = Schedule.query.filter_by(
            description=form.schedule.data).first().id
        return redirect(url_for(
            'schedule.single_schedule', schedule_id=schedule_id)
        )
    return render_template(
        'default-form.html', form=form, title=_('Select Schedule')
    )


@bp.route('/schedule/<schedule_id>')
def single_schedule(schedule_id):
    """Single schedule page"""
    selected_schedule = Schedule.query.filter_by(id=schedule_id).first()
    module = Module.query.filter_by(id=selected_schedule.module).first()
    group = Group.query.filter_by(id=selected_schedule.group).first()
    return render_template(
        'schedule/single_schedule.html', schedule=selected_schedule,
        module=module, group=group, title=_('Schedule')
    )


@bp.route('/api/schedules', methods=['GET'])
@token_auth.login_required
def api_schedule_overview():
    """API call for all schedules"""
    schedules = Schedule.query.all()
    items = []
    for s in schedules:
        items.append(s.to_dict())
    data = {
        '_links': {
            'self': url_for('schedule.api_schedule_overview')
        },
        'items': items
    }
    return jsonify(data)


@bp.route('/api/schedules/schedule/<schedule_id>', methods=['GET'])
@token_auth.login_required
def api_single_schedule(schedule_id):
    """API call for single schedule"""
    s = Schedule.query.filter_by(id=schedule_id).first()
    items = []
    for i in s.items:
        items.append(i.to_dict())
    data = s.to_dict()
    data['items'] = items
    return jsonify(data)


@bp.route('/api/schedules/current')
@token_auth.login_required
def api_current_schedule_items(in_advance=900):
    """API call for all current (and very near future) schedule items"""
    schedule_items = ScheduleItem.query.all()
    items = []
    now = datetime.utcnow()
    for i in schedule_items:
        if not i.start or not i.end:
            pass
        elif now + timedelta(in_advance) >= i.start and now < i.end:
            item = i.to_dict()
            item['_links'] = {
                'schedule': url_for(
                    'schedule.api_single_schedule', schedule_id=i.id)
            }
            items.append(item)
    return jsonify(
        {
            '_links': {
                'self': url_for('schedule.api_current_schedule_items')
                },
            'items': items
        })

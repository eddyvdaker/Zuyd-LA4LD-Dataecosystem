# -*- coding: utf-8 -*-
"""
    schedule.routes
    ~~~~~~~~~~~~~~~

    Routes used for the schedule overview.
"""
from flask import redirect, render_template, url_for

from app.models import Module, Schedule
from app.schedule import bp
from app.schedule.forms import SelectSchedule


@bp.route('/schedule', methods=['GET', 'POST'])
def schedule():
    form = SelectSchedule()
    schedules = Schedule.query.all()
    form.schedule.choices = [
        (x.description, x.description) for x in schedules]
    if form.validate_on_submit():
        schedule_id = Schedule.query.filter_by(
            description=form.schedule.data).first().id
        return redirect(url_for(
            'schedule.single_schedule', schedule_id=schedule_id))
    return render_template('schedule/select_schedule.html', form=form,
                           title='Select Schedule')


@bp.route('/schedule/<schedule_id>')
def single_schedule(schedule_id):
    selected_schedule = Schedule.query.filter_by(id=schedule_id).first()
    module = Module.query.filter_by(id=selected_schedule.module).first()
    return render_template('schedule/single_schedule.html',
                           schedule=selected_schedule, module=module)

# -*- coding: utf-8 -*-
"""
    schedule.forms
    ~~~~~~~~~~~~~~

    Forms that are used inside the schedule blueprint of the application.
"""
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from wtforms.validators import DataRequired


class SelectSchedule(FlaskForm):
    schedule = SelectField('Schedule', validators=[DataRequired()])
    submit = SubmitField('Check')

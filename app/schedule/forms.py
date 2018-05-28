from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from wtforms.validators import DataRequired


class SelectSchedule(FlaskForm):
    schedule = SelectField(_l('Schedule'), validators=[DataRequired()])
    submit = SubmitField(_l('Check'))

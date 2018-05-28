from flask import render_template
from flask_babel import _
from flask_login import current_user, login_required

from app.models import Result
from app.results import bp


@bp.route('/results')
@login_required
def results():
    user = Result.query.filter_by(
        identifier=current_user.hash_identifier())
    user_results = []
    if user:
        for r in user:
            grades = r.grades.all()
            if grades:
                for grade in grades:
                    user_results.append(grade)
    else:
        user_results = None
    return render_template(
        'results/results.html', title=_('Results'), results=user_results
    )



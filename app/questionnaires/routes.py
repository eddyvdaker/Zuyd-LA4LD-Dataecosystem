from flask import render_template, abort
from flask_babel import _
from flask_login import login_required, current_user

from app.models import Questionnaire
from app.questionnaires import bp


@bp.route('/questionnaires', methods=['GET'])
@login_required
def questionnaires():
    user_questionnaires = Questionnaire.query.filter_by(
        identifier=current_user.hash_identifier()
    ).all()
    return render_template(
        'questionnaires/questionnaires.html', title=_('Questionnaires'),
        user_questionnaires=user_questionnaires
    )


@bp.route('/questionnaire/<questionnaire_id>', methods=['GET'])
@login_required
def questionnaire(questionnaire_id):
    q = Questionnaire.query.filter_by(id=questionnaire_id).first_or_404()
    if q.identifier != current_user.hash_identifier():
        abort(403)
    return render_template(
        'questionnaires/questionnaire.html', questionnaire=q,
        title=_('Questionnaire') + f' {q.id}'
    )

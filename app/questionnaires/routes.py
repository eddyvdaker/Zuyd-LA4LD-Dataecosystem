# -*- coding: utf-8 -*-
"""
    app.questionnaires.routes
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Routes for questionnaires functionality
"""
from flask import render_template
from flask_babel import _
from flask_login import login_required, current_user

from app.models import QuestionResult, Questionnaire, QuestionnaireScale, \
    Question
from app.questionnaires import bp


@bp.route('/questionnaires', methods=['GET'])
@login_required
def questionnaires():
    """Give user an overview for his/her questionnaires"""
    user_questions = QuestionResult.query.filter_by(
        identifier=current_user.hash_identifier()
    ).all()
    user_questionnaires = []
    for question in user_questions:
        q = question.result_question.question_scale.scale_questionnaire
        if q not in user_questionnaires:
            user_questionnaires.append(q)
    return render_template(
        'questionnaires/questionnaires.html', title=_('Questionnaires'),
        user_questionnaires=user_questionnaires
    )


@bp.route('/questionnaire/<questionnaire_id>', methods=['GET'])
@login_required
def questionnaire(questionnaire_id):
    """Show results for a single questionnaire"""
    data = Questionnaire.query.filter_by(
        id=questionnaire_id
    ).first().get_questionnaire_for_user(current_user)
    print(data)
    return render_template(
        'questionnaires/questionnaire.html', data=data,
        title=_('Questionnaire') + f' {data["questionnaire"]}'
    )

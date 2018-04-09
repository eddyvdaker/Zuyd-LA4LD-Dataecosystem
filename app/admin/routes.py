# -*- coding: utf-8 -*-
"""
    admin.routes
    ~~~~~~~~~~~~

    Routes used for the admin panel of the application.
"""
import json
import os
from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from secrets import token_urlsafe
from werkzeug.utils import secure_filename

from app import app, db
from app.admin import bp
from app.email import send_new_user_email
from app.main.forms import ImportForm
from app.models import User, Role


def import_users(json_file, mail_details=False):
    """
    When an admin uploads a json file with users, the users will be
    created in the database, a password will be generated, and finally
    the created account details will be send to the user by email.

    :param json_file: <str> path to the json input file
    :param mail_details: <bool> whether the users should receive a mail
        with their account credentials

    :return:
    """
    file = os.path.join(app.config['IMPORT_FOLDER'], json_file)
    with open(file, 'r') as f:
        try:
            users = json.load(f)['users']
        except KeyError:
            flash('Invalid file, missing key "users".')
            return redirect(url_for('admin'))
    user_data = []
    for row in users:
        user = User(username=row['username'], email=row['email'])
        db.session.add(user)
        db.session.commit()

        r = Role.query.filter_by(role=row['role']).first()
        user.role_id = r.id
        db.session.commit()

        password = token_urlsafe()
        user.set_password(password)
        db.session.commit()

        new_user = {'username': user.username,
                    'password': password,
                    'email': user.email}

        if mail_details:
            if 'la4ld-test.com' not in user.email:
                send_new_user_email(new_user)
        else:
            user_data.append(new_user)

    return user_data


@bp.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    user_import_form = ImportForm()
    if current_user.role.role != 'admin':
        abort(403)
    if user_import_form.validate_on_submit():
        f = user_import_form.file.data
        filename = secure_filename(f.filename)
        if not os.path.exists(app.config['IMPORT_FOLDER']):
            os.makedirs(app.config['IMPORT_FOLDER'])
        f.save(os.path.join(app.config['IMPORT_FOLDER'], filename))
        imported_users = import_users(
            os.path.join(app.config['IMPORT_FOLDER'], filename,),
            mail_details=False)
        if imported_users:
            flash('Imported Users (Copy to send to users)')
            for row in imported_users:
                flash(f'User: {row["username"]} ({row["email"]}) - '
                      f'Password: {row["password"]}')
        return redirect(url_for('admin.admin'))

    return render_template('admin/admin.html', title='Admin Panel',
                           user_import_form=user_import_form,)

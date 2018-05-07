# -*- coding: utf-8 -*-
"""
    admin.routes
    ~~~~~~~~~~~~

    Routes used for the admin panel of the application.
"""
import json
import os
from datetime import datetime
from flask import abort, current_app, flash, redirect, render_template, \
    request, url_for, send_file
from flask_login import current_user, login_required
from sqlalchemy.exc import IntegrityError
from secrets import token_urlsafe
from werkzeug.utils import secure_filename

from app import db
from app.admin import bp
from app.admin.forms import ImportForm, EditUserForm, EditModuleForm, \
    EditScheduleForm, EditScheduleItemForm, EditGroupForm
from app.email import send_new_user_email
from app.models import User, Grade, Module, Result, Role, Schedule, \
    ScheduleItem, Group


def upload_file(file):
    """
    Gets the file and filename from the form, makes sure it's secure, and
    saves it to the filesystem.

    :param file: <obj> file object containing the data
    :return: Path to file
    """
    f = file.data
    filename = secure_filename(f.filename)
    if not os.path.exists(current_app.config['IMPORT_FOLDER']):
        os.makedirs(current_app.config['IMPORT_FOLDER'])
    f.save(os.path.join(current_app.config['IMPORT_FOLDER'], filename))

    return os.path.join(current_app.config['IMPORT_FOLDER'], filename,)


def read_json(json_file, field=None):
    """
    Reads the imported json file.

    :param json_file: <str> The path to the json file
    :param field: <str> The field that is search for inside the
        json file, defaults to None
    :return: The json data read from the file
    """
    with open(json_file, 'r') as f:
        if field:
            try:
                data = json.load(f)[field]
            except KeyError:
                flash(f'Invalid file, missing key "{field}"')
                return redirect(url_for('admin'))
        else:
            data = json.load(f)

    return data


def import_users_to_db(data, mail_details=False):
    """
    Writes the data from from the json file to the db

    :param data: <dict> Json data containing the user details
    :param mail_details: <bool> whether the users should receive a mail
        with their account credentials

    :return:
    """

    user_data = []
    users_skipped_data = []
    for row in data:
        try:
            user = User(username=row['username'], email=row['email'],
                        card_number=row['cardnr'])
            db.session.add(user)
            db.session.commit()

            r = Role.query.filter_by(role=row['role']).first()
            user.role_id = r.id
            db.session.commit()

            # Generate random initial password for imported user
            password = token_urlsafe()
            user.set_password(password)
            db.session.commit()
            new_user = {'username': user.username,
                        'password': password,
                        'email': user.email,
                        'cardnr': user.card_number}

            for group in row['groups']:
                user.add_to_group(Group.query.filter_by(
                    code=group).first())
            for module in row['student_of']:
                user.add_to_module(
                    Module.query.filter_by(code=module).first(),
                    module_role='student')
            for module in row['teacher_of']:
                user.add_to_module(
                    Module.query.filter_by(code=module).first(),
                    module_role='teacher')
            for module in row['examiner_of']:
                user.add_to_module(
                    Module.query.filter_by(code=module).first(),
                    module_role='examiner')

            db.session.commit()

            if mail_details:
                if 'la4ld-test.com' not in user.email:
                    send_new_user_email(new_user)
            else:
                user_data.append(new_user)
        except IntegrityError or KeyError:
            db.session.rollback()
            users_skipped_data.append(row['username'])

    return user_data, users_skipped_data


def import_modules_to_db(data):
    """
    Writes the module data from the json file to the db.

    :param data: <dict> Dictionary containing the module data
    :return: Number of imported modules
    """
    for row in data:
        try:
            module = Module(
                code=row['code'],
                name=row['name'],
                description=row['description'],
                start=datetime.strptime(row['start'], '%Y-%m-%d'),
                end=datetime.strptime(row['end'], '%Y-%m-%d'),
                faculty=row['faculty']
            )
            db.session.add(module)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

    return len(data)


def import_results_to_db(data):
    """
    Writes the results data from the json file to the db

    :param data: <dict> Dictionary containing results data
    :return: Number of imported results
    """
    for row in data:
        user = User.query.filter_by(username=row['username']).first()
        module = Module.query.filter_by(code='tm01').order_by(
            Module.start.desc()).first()
        r = Result(identifier=user.hash_identifier(), module=module.id)
        db.session.add(r)
        db.session.commit()

        for grade in row['grades']:
            g = Grade(name=grade['name'], score=grade['score'],
                      weight=grade['weight'], result=r.id)
            db.session.add(g)
            db.session.commit()

    return len(data)


def import_schedules_to_db(data):
    """
    Writes the schedule data from the json file to the db

    :param data: <dict> Dictionary containing schedule data
    :return: Number of imported schedules
    """
    for row in data:
        s = Schedule(description=row['description'])
        grp = Group.query.filter_by(code=row['group']).first()
        s.group = grp.id
        module = Module.query.filter_by(code=row['module']).first()
        s.module = module.id
        db.session.add(s)
        db.session.commit()

        for item in row['items']:
            si = ScheduleItem(
                title=item['title'],
                description=item['description'],
                start=datetime.strptime(item['start'], '%Y-%m-%d %H:%M'),
                end=datetime.strptime(item['end'], '%Y-%m-%d %H:%M'),
                room=item['room'],
                schedule=s.id)
            db.session.add(si)
            db.session.commit()
    return len(data)


def import_groups_to_db(data):
    """
    Writes the group data from the json file to the db

    :param data: <dict> Dictionary containing group data
    :return: Number of imported groups
    """
    for row in data:
        grp = Group(code=row['code'], active=row['active'])
        db.session.add(grp)
        db.session.commit()

        for module in row['modules']:
            grp.add_module_to_group(
                Module.query.filter_by(code=module).first())
        db.session.commit()
    return len(data)


@bp.route('/admin', methods=['GET'])
@login_required
def admin():
    if current_user.role.role != 'admin':
        abort(403)
    return render_template('admin/admin.html', title='Admin Panel')


@bp.route('/admin/users_import', methods=['GET', 'POST'])
@login_required
def import_users():
    if current_user.role.role != 'admin':
        abort(403)
    form = ImportForm()
    if form.validate_on_submit():
        file = upload_file(form.file)
        user_data = read_json(file, field='users')
        imported_users, skipped_users = import_users_to_db(user_data)
        flash(f'Imported {len(imported_users)} of {len(user_data)} Users.')
        current_app.logger.info(f'User Import: imported {len(imported_users)}'
                                f' of {len(user_data)} users')
        if imported_users:
            flash('Imported Users (Copy to send to users):')
            for row in imported_users:
                flash(f'User: {row["username"]} (email: {row["email"]}, card:'
                      f' {row["cardnr"]}) - Password: {row["password"]}')
        if skipped_users:
            flash('Skipped Users:')
            for row in skipped_users:
                flash(f'{row} skipped')

        return redirect(url_for('admin.admin'))
    return render_template(
        'admin/import.html', title='Admin Panel: Import Users', form=form,
        example_gist_code='f73e48eea2c3672dec92adc2dd2627ef')


@bp.route('/admin/users_overview', methods=['GET'])
@login_required
def users_overview():
    if current_user.role.role != 'admin':
        abort(403)
    users = User.query.all()
    return render_template(
        'admin/users_overview.html', title='Admin Panel: Users Overview',
        users=users)


@bp.route('/admin/user/<user_id>', methods=['GET'])
@login_required
def single_user(user_id):
    if current_user.role.role != 'admin':
        abort(403)
    user = User.query.filter_by(id=user_id).first()
    groups = user.groups_of_student()
    for i, group in enumerate(groups):
        groups[i].modules_list = ', '.join(map(
            str, [x.code for x in group.get_modules_of_group()]))
    return render_template(
        'admin/single_user.html', title=f'Admin Panel: User {user_id}',
        user=user, groups=groups)


@bp.route('/admin/edit_user/<user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    if current_user.role.role != 'admin':
        abort(403)
    form = EditUserForm()
    roles = Role.query.all()
    form.role.choices = [(x.role, x.role) for x in roles]
    user = User.query.filter_by(id=user_id).first()
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.role = Role.query.filter_by(role=form.role.data).first()
        user.card_number = form.card_number.data
        db.session.commit()
        flash('The changes have been saved.')
        return redirect(url_for('admin.single_user', user_id=user.id))
    elif request.method == 'GET':
        form.username.data = user.username
        form.email.data = user.email
        form.role.data = user.role.role
        form.card_number.data = user.card_number
    return render_template(
        'admin/edit_user.html', form=form, title='Admin Panel: Edit User')


@bp.route('/admin/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    if current_user.role.role != 'admin':
        abort(403)
    form = EditUserForm()
    roles = Role.query.all()
    form.role.choices = [(x.role, x.role) for x in roles]
    if form.validate_on_submit():
        u = User(
            username=form.username.data,
            email=form.email.data,
            role=Role.query.filter_by(role=form.role.data).first(),
            card_number=form.card_number.data)
        db.session.add(u)
        db.session.commit()
        return redirect(url_for('admin.users_overview'))
    return render_template(
        'admin/edit_user.html', form=form, title='Admin Panel: New User')


@bp.route('/admin/modules_import', methods=['GET', 'POST'])
@login_required
def import_modules():
    if current_user.role.role != 'admin':
        abort(403)
    form = ImportForm()
    if form.validate_on_submit():
        file = upload_file(form.file)
        module_data = read_json(file, field='modules')
        import_status = import_modules_to_db(module_data)
        flash(f'{import_status} modules imported')
        current_app.logger.info(f'{import_status} modules imported')
        return redirect(url_for('admin.admin'))
    return render_template(
        'admin/import.html', title='Admin Panel: Import Modules',
        form=form, example_gist_code='3c1848ce491d9061fec9ae18ae5069e0')


@bp.route('/admin/modules_overview', methods=['GET'])
@login_required
def modules_overview():
    if current_user.role.role != 'admin':
        abort(403)
    modules = Module.query.all()
    return render_template(
        'admin/modules_overview.html', title='Admin Panel: Modules Overview',
        modules=modules)


@bp.route('/admin/edit_module/<module_id>', methods=['GET', 'POST'])
@login_required
def edit_module(module_id):
    if current_user.role.role != 'admin':
        abort(403)
    form = EditModuleForm()
    module = Module.query.filter_by(id=module_id).first()
    if form.validate_on_submit():
        module.code = form.code.data
        module.name = form.description.data
        module.description = form.description.data
        module.start = form.start.data
        module.end = form.end.data
        module.faculty = form.faculty.data
        db.session.commit()
        flash('The changes have been saved.')
        return redirect(url_for('admin.modules_overview'))
    elif request.method == 'GET':
        form.code.data = module.code
        form.name.data = module.name
        form.description.data = module.description
        form.start.data = module.start
        form.end.data = module.end
        form.faculty.data = module.faculty
    return render_template('admin/edit_module.html', form=form)


@bp.route('/admin/add_module', methods=['GET', 'POST'])
@login_required
def add_module():
    if current_user.role.role != 'admin':
        abort(403)
    form = EditModuleForm()
    if form.validate_on_submit():
        m = Module(
            code=form.code.data,
            name=form.name.data,
            description=form.description.data,
            start=form.start.data,
            end=form.end.data,
            faculty=form.faculty.data)
        db.session.add(m)
        db.session.commit()
        return redirect(url_for('admin.modules_overview'))
    return render_template(
        'admin/edit_module.html', form=form, title='Admin Panel: Add Module')


@bp.route('/admin/results_import', methods=['GET', 'POST'])
@login_required
def import_results():
    if current_user.role.role != 'admin':
        abort(403)
    form = ImportForm()
    if form.validate_on_submit():
        file = upload_file(form.file)
        results_data = read_json(file, field='results')
        import_status = import_results_to_db(results_data)
        flash(f'{import_status} results imported')
        current_app.logger.info(f'{import_status} results imported')
        return redirect(url_for('admin.admin'))
    return render_template(
        'admin/import.html', title='Admin Panel: Import Results', form=form,
        example_gist_code='d504fb80b48c28e2e1495e76ea33814e')


@bp.route('/admin/group_overview', methods=['GET'])
@login_required
def group_overview():
    if current_user.role.role != 'admin':
        abort(403)
    groups = Group.query.all()
    for i, group in enumerate(groups):
        groups[i].modules_list = ', '.join(map(
            str, [x.code for x in group.get_modules_of_group()]))
    return render_template(
        'admin/group_overview.html', title='Admin Panel: Group Overview',
        groups=groups)


@bp.route('/admin/group/<group_id>', methods=['GET'])
@login_required
def single_group(group_id):
    if current_user.role.role != 'admin':
        abort(403)
    group = Group.query.filter_by(id=group_id).first()
    return render_template(
        'admin/single_group.html', title=f'Admin Panel: Group {group.id}',
        group=group,
    )


@bp.route('/admin/group_import', methods=['GET', 'POST'])
@login_required
def import_group():
    if current_user.role.role != 'admin':
        abort(403)
    form = ImportForm()
    if form.validate_on_submit():
        file = upload_file(form.file)
        group_data = read_json(file, field='groups')
        import_status = import_groups_to_db(group_data)
        flash(f'{import_status} groups imported')
        current_app.logger.info(f'{import_status} groups imported')
        return redirect(url_for('admin.admin'))
    return render_template(
        'admin/import.html', title='Admin Panel: Import Groups', form=form,
        example_gist_code='b410ae801de3fae1d8ab6ec4347a6800')


@bp.route('/admin/add_group', methods=['GET', 'POST'])
@login_required
def add_group():
    if current_user.role.role != 'admin':
        abort(403)
    form = EditGroupForm()
    if form.validate_on_submit():
        group = Group(code=form.code.data, active=form.active.data)
        db.session.add(group)
        db.session.commit()
        flash(f'Group {form.code.data} with id {group.id} added')
        redirect(url_for('admin.group_overview'))
    return render_template(
        'admin/edit_group.html', title='Admin Panel: Add Group', form=form)


@bp.route('/admin/edit_group/<group_id>', methods=['GET', 'POST'])
@login_required
def edit_group(group_id):
    if current_user.role.role != 'admin':
        abort(403)
    form = EditGroupForm()
    group = Group.query.filter_by(id=group_id).first()
    if form.validate_on_submit():
        group.code = form.code.data
        group.active = form.active.data
        db.session.commit()
        flash(f'Group {form.code.data} with id {group.id} updated')
        return redirect(url_for('admin.single_group', group_id=group_id))
    else:
        form.code.data = group.code
        form.active.data = group.active
    return render_template(
        'admin/edit_group.html', title='Admin Panel: Edit Group', form=form)


@bp.route('/admin/schedule_import', methods=['GET', 'POST'])
@login_required
def import_schedule():
    if current_user.role.role != 'admin':
        abort(403)
    form = ImportForm()
    if form.validate_on_submit():
        file = upload_file(form.file)
        schedule_data = read_json(file, field='schedules')
        import_status = import_schedules_to_db(schedule_data)
        flash(f'{import_status} schedules imported')
        current_app.logger.info(f'{import_status} schedules imported')
        return redirect(url_for('admin.admin'))
    return render_template(
        'admin/import.html', title='Admin Panel: Import Schedules', form=form,
        example_gist_code='b410ae801de3fae1d8ab6ec4347a6800')


@bp.route('/admin/schedule_overview', methods=['GET'])
@login_required
def schedule_overview():
    if current_user.role.role != 'admin':
        abort(403)
    schedules = Schedule.query.all()
    return render_template(
        'admin/schedule_overview.html', title='Admin Panel: Schedule Overview',
        schedules=schedules)


@bp.route('/admin/schedule/<schedule_id>', methods=['GET'])
@login_required
def single_schedule(schedule_id):
    if current_user.role.role != 'admin':
        abort(403)
    schedule = Schedule.query.filter_by(id=schedule_id).first()
    module = Module.query.filter_by(id=schedule.module).first()
    group = Group.query.filter_by(id=schedule.group).first()
    return render_template(
        'admin/single_schedule.html', schedule=schedule, group=group,
        title=f'Admin Panel: Schedule {schedule_id}', module=module)


@bp.route('/admin/edit_schedule/<schedule_id>', methods=['GET', 'POST'])
@login_required
def edit_schedule(schedule_id):
    if current_user.role.role != 'admin':
        abort(403)
    form = EditScheduleForm()
    schedule = Schedule.query.filter_by(id=schedule_id).first()
    modules = Module.query.all()
    form.module.choices = [
        (int(x.id), f'{x.id}: {x.code} ({x.start}-{x.end}') for x in modules]
    groups = Group.query.all()
    form.group.choices = [
        (int(x.id), f'{x.id}: {x.code} ({x.active})') for x in groups]
    if form.validate_on_submit():
        schedule.description = form.description.data
        schedule.module = form.module.data
        schedule.group = form.group.data
        db.session.commit()
        return redirect(url_for(
            'admin.single_schedule', schedule_id=schedule_id))
    elif request.method == 'GET':
        form.description.data = schedule.description
        form.module.data = schedule.module
        form.group.data = schedule.group
    return render_template(
        'admin/edit_schedule.html', title='Admin Panel: Edit Schedule',
        form=form)


@bp.route('/admin/add_schedule', methods=['GET', 'POST'])
@login_required
def add_schedule():
    if current_user.role.role != 'admin':
        abort(403)
    form = EditScheduleForm()
    modules = Module.query.all()
    form.module.choices = [
        (int(x.id), f'{x.id}: {x.code} ({x.start}-{x.end}') for x in modules]
    groups = Group.query.all()
    form.group.choices = [
        (int(x.id), f'{x.id}: {x.code} ({x.active})') for x in groups]
    if form.validate_on_submit():
        s = Schedule(
            description=form.description.data,
            module=form.module.data,
            group=form.group.data)
        db.session.add(s)
        db.session.commit()
        return redirect(url_for('admin.schedule_overview'))
    return render_template(
        'admin/edit_schedule.html', title='Admin Panel: Add Schedule',
        form=form)


@bp.route(
    '/admin/edit_schedule/<schedule_id>/<item_id>', methods=['GET', 'POST'])
@login_required
def edit_schedule_item(schedule_id, item_id):
    if current_user.role.role != 'admin':
        abort(403)
    form = EditScheduleItemForm()
    item = ScheduleItem.query.filter_by(id=item_id).first()
    if form.validate_on_submit():
        item.title = form.title.data
        item.description = form.description.data
        item.start = form.start.data
        item.end = form.end.data
        item.room = form.room.data
        db.session.commit()
        return redirect(url_for(
            'admin.single_schedule', schedule_id=schedule_id))
    elif request.method == 'GET':
        form.title.data = item.title
        form.description.data = item.description
        form.start.data = item.start
        form.end.data = item.end
        form.room.data = item.room
    return render_template(
        'admin/edit_schedule_item.html', form=form,
        title='Admin Panel:Edit Schedule Item')


@bp.route(
    '/admin/add_schedule_item/<schedule_id>', methods=['GET', 'POST'])
@login_required
def add_schedule_item(schedule_id):
    if current_user.role.role != 'admin':
        abort(403)
    form = EditScheduleItemForm()
    schedule = Schedule.query.filter_by(id=schedule_id).first()
    if form.validate_on_submit():
        si = ScheduleItem(
            title=form.title.data,
            description=form.description.data,
            start=form.start.data,
            end=form.end.data,
            room=form.room.data,
            schedule=schedule.id)
        db.session.add(si)
        db.session.commit()
        return redirect(url_for(
            'admin.single_schedule', schedule_id=schedule_id))
    return render_template(
        'admin/edit_schedule_item.html', form=form,
        title='Admin Panel: New Schedule Item')


@bp.route('/admin/logs', methods=['GET'])
@login_required
def show_logs():
    if current_user.role.role != 'admin':
        abort(403)
    base_dir = os.path.abspath(os.path.dirname('__main__'))
    log_file = os.path.join(base_dir, 'logs/la4ld.log')
    with open(log_file, 'r') as f:
        log_data = f.read().splitlines()

    return render_template(
        'admin/logs.html', title='Admin Panel: Logs', logs=log_data)


@bp.route('/downloads/logs', methods=['GET'])
@login_required
def download_logs():
    if current_user.role.role != 'admin':
        abort(403)
    else:
        base_dir = os.path.abspath(os.path.dirname('__main__'))
        log_file = os.path.join(base_dir, 'logs/la4ld.log')
        return send_file(
            log_file,
            mimetype='text/plain',
            attachment_filename='la4ld.log',
            as_attachment=True,
            cache_timeout=-1)


@bp.route('/admin/fact-store', methods=['GET'])
@login_required
def show_fact_store():
    if current_user.role.role != 'admin':
        abort(403)
    base_dir = os.path.abspath(os.path.dirname('__main__'))
    fact_store_file = os.path.join(base_dir, current_app.config['FACT_STORE'])
    try:
        with open(fact_store_file, 'r') as f:
            fact_store_data = f.read().splitlines()
    except FileNotFoundError:
        fact_store_data = ['No Fact-Store Data']

    return render_template(
        'admin/fact-store.html', title='Admin Panel: Fact-Store',
        fact_store=fact_store_data)


@bp.route('/downloads/fact-store', methods=['GET'])
@login_required
def download_fact_store():
    if current_user.role.role != 'admin':
        abort(403)
    else:

        base_dir = os.path.abspath(os.path.dirname('__main__'))
        fact_store_file = os.path.join(
            base_dir, current_app.config['FACT_STORE'])
        if os.path.exists(fact_store_file):
            return send_file(
                fact_store_file,
                mimetype='text/plain',
                attachment_filename='fact-store.txt',
                as_attachment=True,
                cache_timeout=-1)
        else:
            flash('No Fact-Store data available')
            return redirect(url_for('admin.show_fact_store'))

# -*- coding: utf-8 -*-
"""
    admin.routes
    ~~~~~~~~~~~~

    Routes used for the admin panel of the application.
"""
import os
from secrets import token_urlsafe
from flask import current_app, flash, redirect, render_template, \
    request, url_for, send_file
from flask_babel import _
from flask_login import login_required

from app import db
from app.admin import bp
from app.admin.forms import ImportForm, EditUserForm, EditModuleForm, \
    EditScheduleForm, EditScheduleItemForm, EditGroupForm, \
    ManageGroupMembershipForm, ManageModuleMembershipForm, AddApiKeyForm, \
    ApiKeyDeleteConfirmationForm
from app.admin.imports import upload_file, import_groups_to_db, \
    import_modules_to_db, import_results_to_db, import_schedules_to_db, \
    import_users_to_db, read_json
from app.auth.decorator import admin_required
from app.models import User, Module, Role, Schedule, ScheduleItem, Group, \
    ApiKey


@bp.route('/admin', methods=['GET'])
@login_required
@admin_required
def admin():
    return render_template('admin/admin.html', title=_('Admin Panel'))


@bp.route('/admin/users_import', methods=['GET', 'POST'])
@login_required
@admin_required
def import_users():
    form = ImportForm()
    if form.validate_on_submit():
        file = upload_file(form.file)
        user_data = read_json(file, field='users')
        imported_users, skipped_users = import_users_to_db(user_data)
        # STRING NOT TRANSLATED YET (STR WITH VARIABLES)
        flash(f'Imported {len(imported_users)} of {len(user_data)} Users.')
        current_app.logger.info(f'User Import: imported {len(imported_users)}'
                                f' of {len(user_data)} users')
        if imported_users:
            flash(_('Imported Users (Copy to send to users):'))
            for row in imported_users:
                # STRING NOT TRANSLATED YET (STR WITH VARIABLES)
                flash(
                    f'User: {row["username"]} (email: {row["email"]}, card:'
                    f' {row["cardnr"]}) - Password: {row["password"]}'
                )
        if skipped_users:
            flash(_('Skipped Users:'))
            for row in skipped_users:
                # STRING NOT TRANSLATED YET (STR WITH VARIABLES)
                flash(f'{row} skipped')

        return redirect(url_for('admin.admin'))
    return render_template(
        'admin/import.html', title=_('Admin Panel: Import Users'), form=form,
        example_gist_code='f73e48eea2c3672dec92adc2dd2627ef'
    )


@bp.route('/admin/users_overview', methods=['GET'])
@login_required
@admin_required
def users_overview():
    users = User.query.all()
    return render_template(
        'admin/users_overview.html', title=_('Admin Panel: Users Overview'),
        users=users
    )


@bp.route('/admin/user/<user_id>', methods=['GET'])
@login_required
@admin_required
def single_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    groups = user.groups_of_student()
    for i, group in enumerate(groups):
        groups[i].modules_list = ', '.join(map(
            str, [x.code for x in group.get_modules_of_group()]))
    return render_template(
        'admin/single_user.html', user=user, groups=groups,
        title=_(f'Admin Panel: User ') + str(user_id)
    )


@bp.route('/admin/edit_user/<user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(user_id):
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
        flash(_('The changes have been saved.'))
        return redirect(url_for('admin.single_user', user_id=user.id))
    elif request.method == 'GET':
        form.username.data = user.username
        form.email.data = user.email
        form.role.data = user.role.role
        form.card_number.data = user.card_number
    return render_template(
        'default-form.html', form=form, title=_('Admin Panel: Edit User')
    )


@bp.route('/admin/add_user', methods=['GET', 'POST'])
@login_required
@admin_required
def add_user():
    form = EditUserForm()
    roles = Role.query.all()
    form.role.choices = [(x.role, x.role) for x in roles]
    if form.validate_on_submit():
        # noinspection PyArgumentList
        u = User(
            username=form.username.data,
            email=form.email.data,
            role=Role.query.filter_by(role=form.role.data).first(),
            card_number=form.card_number.data)
        db.session.add(u)
        db.session.commit()
        return redirect(url_for('admin.users_overview'))
    return render_template(
        'default-form.html', form=form, title=_('Admin Panel: New User')
    )


@bp.route('/admin/modules_import', methods=['GET', 'POST'])
@login_required
@admin_required
def import_modules():
    form = ImportForm()
    if form.validate_on_submit():
        file = upload_file(form.file)
        module_data = read_json(file, field='modules')
        import_status = import_modules_to_db(module_data)
        flash(import_status + _(' modules imported'))
        current_app.logger.info(f'{import_status} modules imported')
        return redirect(url_for('admin.admin'))
    return render_template(
        'admin/import.html', title=_('Admin Panel: Import Modules'),
        form=form, example_gist_code='3c1848ce491d9061fec9ae18ae5069e0'
    )


@bp.route('/admin/modules_overview', methods=['GET'])
@login_required
@admin_required
def modules_overview():
    modules = Module.query.all()
    return render_template(
        'admin/modules_overview.html', modules=modules,
        title=_('Admin Panel: Modules Overview')
    )


@bp.route('/admin/edit_module/<module_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_module(module_id):
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
        flash(_('The changes have been saved.'))
        return redirect(url_for('admin.modules_overview'))
    elif request.method == 'GET':
        form.code.data = module.code
        form.name.data = module.name
        form.description.data = module.description
        form.start.data = module.start
        form.end.data = module.end
        form.faculty.data = module.faculty
    return render_template(
        'default-form.html', form=form,
        title=_('Admin Panel: Edit Module')
    )


@bp.route('/admin/add_module', methods=['GET', 'POST'])
@login_required
@admin_required
def add_module():
    form = EditModuleForm()
    if form.validate_on_submit():
        m = Module(
            code=form.code.data,
            name=form.name.data,
            description=form.description.data,
            start=form.start.data,
            end=form.end.data,
            faculty=form.faculty.data
        )
        db.session.add(m)
        db.session.commit()
        return redirect(url_for('admin.modules_overview'))
    return render_template(
        'default-form.html', form=form,
        title=_('Admin Panel: Add Module')
    )


@bp.route('/admin/results_import', methods=['GET', 'POST'])
@login_required
@admin_required
def import_results():
    form = ImportForm()
    if form.validate_on_submit():
        file = upload_file(form.file)
        results_data = read_json(file, field='results')
        import_status = import_results_to_db(results_data)
        flash(import_status + _(f' results imported'))
        current_app.logger.info(f'{import_status} results imported')
        return redirect(url_for('admin.admin'))
    return render_template(
        'admin/import.html', title=_('Admin Panel: Import Results'), form=form,
        example_gist_code='d504fb80b48c28e2e1495e76ea33814e'
    )


@bp.route('/admin/group_overview', methods=['GET'])
@login_required
@admin_required
def group_overview():
    groups = Group.query.all()
    for i, group in enumerate(groups):
        groups[i].modules_list = ', '.join(map(
            str, [x.code for x in group.get_modules_of_group()])
        )
    return render_template(
        'admin/group_overview.html', title=_('Admin Panel: Group Overview'),
        groups=groups)


@bp.route('/admin/group/<group_id>', methods=['GET'])
@login_required
@admin_required
def single_group(group_id):
    group = Group.query.filter_by(id=group_id).first()
    return render_template(
        'admin/single_group.html', group=group,
        title=_(f'Admin Panel: Group ') + str(group.id)
    )


@bp.route('/admin/group_import', methods=['GET', 'POST'])
@login_required
@admin_required
def import_group():
    form = ImportForm()
    if form.validate_on_submit():
        file = upload_file(form.file)
        group_data = read_json(file, field='groups')
        import_status = import_groups_to_db(group_data)
        flash(import_status + _(f' groups imported'))
        current_app.logger.info(f'{import_status} groups imported')
        return redirect(url_for('admin.admin'))
    return render_template(
        'admin/import.html', title=_('Admin Panel: Import Groups'), form=form,
        example_gist_code='b410ae801de3fae1d8ab6ec4347a6800'
    )


@bp.route('/admin/add_group', methods=['GET', 'POST'])
@login_required
@admin_required
def add_group():
    form = EditGroupForm()
    if form.validate_on_submit():
        group = Group(code=form.code.data, active=form.active.data)
        db.session.add(group)
        db.session.commit()
        # STRING NOT TRANSLATED YET (STR WITH VARIABLES)
        flash(f'Group {form.code.data} with id {group.id} added')
        redirect(url_for('admin.group_overview'))
    return render_template(
        'default-form.html', title=_('Admin Panel: Add Group'), form=form
    )


@bp.route('/admin/edit_group/<group_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_group(group_id):
    form = EditGroupForm()
    group = Group.query.filter_by(id=group_id).first()
    if form.validate_on_submit():
        group.code = form.code.data
        group.active = form.active.data
        db.session.commit()
        # STRING NOT TRANSLATED YET (STR WITH VARIABLES)
        flash(f'Group {form.code.data} with id {group.id} updated')
        return redirect(url_for('admin.single_group', group_id=group_id))
    else:
        form.code.data = group.code
        form.active.data = group.active
    return render_template(
        'default-form.html', title=_('Admin Panel: Edit Group'), form=form
    )


@bp.route('/admin/schedule_import', methods=['GET', 'POST'])
@login_required
@admin_required
def import_schedule():
    form = ImportForm()
    if form.validate_on_submit():
        file = upload_file(form.file)
        schedule_data = read_json(file, field='schedules')
        import_status = import_schedules_to_db(schedule_data)
        flash(import_status + _(f' schedules imported'))
        current_app.logger.info(import_status + _(f' schedules imported'))
        return redirect(url_for('admin.admin'))
    return render_template(
        'admin/import.html', title=_('Admin Panel: Import Schedules'),
        form=form, example_gist_code='b410ae801de3fae1d8ab6ec4347a6800'
    )


@bp.route('/admin/schedule_overview', methods=['GET'])
@login_required
@admin_required
def schedule_overview():
    schedules = Schedule.query.all()
    return render_template(
        'admin/schedule_overview.html',
        title=_('Admin Panel: Schedule Overview'), schedules=schedules
    )


@bp.route('/admin/schedule/<schedule_id>', methods=['GET'])
@login_required
@admin_required
def single_schedule(schedule_id):
    schedule = Schedule.query.filter_by(id=schedule_id).first()
    module = Module.query.filter_by(id=schedule.module).first()
    group = Group.query.filter_by(id=schedule.group).first()
    return render_template(
        'admin/single_schedule.html', schedule=schedule, group=group,
        title=_(f'Admin Panel: ') + str(schedule_id), module=module
    )


@bp.route('/admin/edit_schedule/<schedule_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_schedule(schedule_id):
    form = EditScheduleForm()
    schedule = Schedule.query.filter_by(id=schedule_id).first()
    modules = Module.query.all()
    form.module.choices = [
        (int(x.id), f'{x.id}: {x.code} ({x.start}-{x.end}') for x in modules
    ]
    groups = Group.query.all()
    form.group.choices = [
        (int(x.id), f'{x.id}: {x.code} ({x.active})') for x in groups
    ]
    if form.validate_on_submit():
        schedule.description = form.description.data
        schedule.module = form.module.data
        schedule.group = form.group.data
        db.session.commit()
        return redirect(url_for(
            'admin.single_schedule', schedule_id=schedule_id)
        )
    elif request.method == 'GET':
        form.description.data = schedule.description
        form.module.data = schedule.module
        form.group.data = schedule.group
    return render_template(
        'default-form.html', title=_('Admin Panel: Edit Schedule'),
        form=form
    )


@bp.route('/admin/add_schedule', methods=['GET', 'POST'])
@login_required
@admin_required
def add_schedule():
    form = EditScheduleForm()
    modules = Module.query.all()
    form.module.choices = [
        (int(x.id), f'{x.id}: {x.code} ({x.start}-{x.end}') for x in modules
    ]
    groups = Group.query.all()
    form.group.choices = [
        (int(x.id), f'{x.id}: {x.code} ({x.active})') for x in groups
    ]
    if form.validate_on_submit():
        s = Schedule(
            description=form.description.data,
            module=form.module.data,
            group=form.group.data)
        db.session.add(s)
        db.session.commit()
        return redirect(url_for('admin.schedule_overview'))
    return render_template(
        'default-form.html', title=_('Admin Panel: Add Schedule'),
        form=form
    )


@bp.route(
    '/admin/edit_schedule/<schedule_id>/<item_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_schedule_item(schedule_id, item_id):
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
            'admin.single_schedule', schedule_id=schedule_id)
        )
    elif request.method == 'GET':
        form.title.data = item.title
        form.description.data = item.description
        form.start.data = item.start
        form.end.data = item.end
        form.room.data = item.room
    return render_template(
        'default-form.html', form=form,
        title=_('Admin Panel:Edit Schedule Item')
    )


@bp.route(
    '/admin/add_schedule_item/<schedule_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def add_schedule_item(schedule_id):
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
            'admin.single_schedule', schedule_id=schedule_id)
        )
    return render_template(
        'default-form.html', form=form,
        title=_('Admin Panel: New Schedule Item')
    )


@bp.route('/admin/logs', methods=['GET'])
@login_required
@admin_required
def show_logs():
    base_dir = os.path.abspath(os.path.dirname('__main__'))
    log_file = os.path.join(base_dir, 'logs/la4ld.log')
    with open(log_file, 'r') as f:
        log_data = f.read().splitlines()

    return render_template(
        'admin/logs.html', title=_('Admin Panel: Logs'), logs=log_data
    )


@bp.route('/downloads/logs', methods=['GET'])
@login_required
@admin_required
def download_logs():
    base_dir = os.path.abspath(os.path.dirname('__main__'))
    log_file = os.path.join(base_dir, 'logs/la4ld.log')
    return send_file(
        log_file,
        mimetype='text/plain',
        attachment_filename='la4ld.log',
        as_attachment=True,
        cache_timeout=-1
    )


@bp.route('/admin/fact-store', methods=['GET'])
@login_required
@admin_required
def show_fact_store():
    base_dir = os.path.abspath(os.path.dirname('__main__'))
    fact_store_file = os.path.join(base_dir, current_app.config['FACT_STORE'])
    try:
        with open(fact_store_file, 'r') as f:
            fact_store_data = f.read().splitlines()
    except FileNotFoundError:
        fact_store_data = [_('No Fact-Store Data')]

    return render_template(
        'admin/fact-store.html', title=_('Admin Panel: Fact-Store'),
        fact_store=fact_store_data
    )


@bp.route('/downloads/fact-store', methods=['GET'])
@login_required
@admin_required
def download_fact_store():
    base_dir = os.path.abspath(os.path.dirname('__main__'))
    fact_store_file = os.path.join(
        base_dir, current_app.config['FACT_STORE'])
    if os.path.exists(fact_store_file):
        return send_file(
            fact_store_file,
            mimetype='text/plain',
            attachment_filename='fact-store.txt',
            as_attachment=True,
            cache_timeout=-1
        )
    else:
        flash(_('No Fact-Store data available'))
        return redirect(url_for('admin.show_fact_store'))


@bp.route('/admin/manage-groups', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_group_membership():
    groups = Group.query.all()
    users = User.query.all()
    form = ManageGroupMembershipForm()
    form.users_list.choices = [(x.id, x.username) for x in users]
    form.groups_list.choices = [(x.id, x.code) for x in groups]
    if request.method == 'POST':
        for user_id in form.users_list.data:
            user = User.query.filter_by(id=user_id).first()
            for group_id in form.groups_list.data:
                group = Group.query.filter_by(id=group_id).first()
                if form.action.data == 'add':
                    user.add_to_group(group)
                    flash(_('Added users to groups.'))
                elif form.action.data == 'remove':
                    user.remove_from_group(group)
                    flash(_('Removed users from groups'))
            db.session.commit()
        return redirect(url_for('admin.manage_group_membership'))
    return render_template(
        'admin/manage_groups.html', title=_('Admin Panel: Manage Groups'),
        form=form
    )


@bp.route('/admin/manage-modules', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_module_membership():
    modules = Module.query.all()
    users = User.query.all()
    form = ManageModuleMembershipForm()
    form.users_list.choices = [(x.id, x.username) for x in users]
    form.modules_list.choices = [
        (x.id, f'{x.id}: {x.code} ({x.start}-{x.end})') for x in modules]
    form.roles.choices = [
        ('student', 'student'),
        ('teacher', 'teacher'),
        ('examiner', 'examiner')
    ]
    if request.method == 'POST':
        for user_id in form.users_list.data:
            user = User.query.filter_by(id=user_id).first()
            for module_id in form.modules_list.data:
                module = Module.query.filter_by(id=module_id).first()
                if form.action.data == 'add':
                    user.add_to_module(module, module_role=form.roles.data)
                    # STRING NOT TRANSLATED YET (STR WITH VARIABLES)
                    flash(f'Added {form.roles.data} to modules')
                elif form.action.data == 'remove':
                    user.remove_from_module(
                        module, module_role=form.roles.data)
                    # STRING NOT TRANSLATED YET (STR WITH VARIABLES)
                    flash(f'Removed {form.roles.data} from modules')
            db.session.commit()
        return redirect(url_for('admin.manage_module_membership'))
    return render_template(
        'admin/manage_modules.html', title=_('Admin Panel: Manage Modules'),
        form=form
    )


@bp.route('/admin/apikey-overview', methods=['GET'])
@login_required
@admin_required
def apikey_overview():
    return render_template(
        'admin/overview_api_keys.html', keys=ApiKey.query.all(),
        title=_('Admin Panel: API Key Overview')
    )


@bp.route('/admin/add-apikey', methods=['GET', 'POST'])
@login_required
@admin_required
def add_apikey():
    form = AddApiKeyForm()
    if form.validate_on_submit():
        a = ApiKey(key=form.key.data, description=form.description.data)
        db.session.add(a)
        db.session.commit()
        return redirect(url_for('admin.apikey_overview'))
    else:
        while form.key.data in [x.key for x in ApiKey.query.all()] or \
                not form.key.data:
            form.key.data = token_urlsafe(24)
    return render_template(
        'default-form.html', form=form, title=_('Admin Panel: Add API Key')
    )


@bp.route('/admin/delete-apikey/<key_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def delete_apikey(key_id):
    form = ApiKeyDeleteConfirmationForm()
    key = ApiKey.query.filter_by(id=key_id).first()
    if form.validate_on_submit():
        ApiKey.query.filter_by(id=key.id).delete()
        db.session.commit()
        flash(_('API key deleted'))
        return redirect(url_for('admin.apikey_overview'))
    return render_template(
        'admin/delete_api_key.html', form=form, key=key,
        title=_('Admin Panel: Delete API Key')
    )

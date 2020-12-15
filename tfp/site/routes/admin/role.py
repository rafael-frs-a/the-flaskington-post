from flask import Blueprint, flash, render_template, redirect, url_for, request, session
from tfp.ext.database import db
from tfp.site.forms.admin.role_form import RoleForm
from tfp.site.models.user import Role, User, get_roles

admin_role_route = Blueprint('admin_role_route', __name__)


def route_role_form(role):
    try:
        form_data = session.pop('role-form-data')
        form_errors = session.pop('role-form-errors')
    except KeyError:
        form = RoleForm()

        if role:
            form.name.data = role.name
            form.description.data = role.description

        return render_template('admin/role_form.html', title='Role',
                               form=form, url_back=url_for('admin_role_route.role'))

    form = RoleForm(data=form_data)
    return render_template('admin/role_form.html', title='Role', form=form,
                           errors=form_errors, url_back=url_for('admin_role_route.role'))


@admin_role_route.route('/admin/role')
def role():
    page = request.args.get('page', 1, type=int)
    sort = request.args.get('sort')
    desc = request.args.get('desc')
    per_page = 10

    if sort:
        roles = get_roles(per_page, page, sort, desc)
    else:
        roles = get_roles(per_page, page, 'id', True)

    return render_template('admin/role.html', title='Role', roles=roles)


@admin_role_route.route('/admin/role/new', methods=['GET'])
def new_role():
    return route_role_form(None)


@admin_role_route.route('/admin/role/new', methods=['POST'])
def new_role_prg():
    form = RoleForm()

    if form.validate_on_submit():
        role = Role(name=form.name.data, description=form.description.data)
        db.session.add(role)
        db.session.commit()

        return redirect(url_for('admin_role_route.role'))

    session['role-form-data'] = form.data
    session['role-form-errors'] = form.errors
    return redirect(url_for('admin_role_route.new_role'))


@admin_role_route.route('/admin/role/<name>', methods=['GET'])
def edit_role(name):
    role = Role.query.filter_by(name=name).first_or_404()
    return route_role_form(role)


@admin_role_route.route('/admin/role/<name>', methods=['POST'])
def edit_role_prg(name):
    role = Role.query.filter_by(name=name).first_or_404()
    form = RoleForm()
    form.current_role = role

    if form.validate_on_submit():
        role.name = form.name.data
        role.description = form.description.data
        db.session.commit()

        return redirect(url_for('admin_role_route.role'))

    session['role-form-data'] = form.data
    session['role-form-errors'] = form.errors
    return redirect(url_for('admin_role_route.edit_role', name=name))


@admin_role_route.route('/admin/role/delete/<name>', methods=['POST'])
def delete_role(name):
    role = Role.query.filter_by(name=name).first_or_404()
    user = User.query.filter(User.roles.any(name=name)).first()

    if user:
        flash('This role cannot be deleted. There are still users using it.', 'danger')
    else:
        db.session.delete(role)
        db.session.commit()

    return redirect(request.referrer if request.referrer else url_for('admin_role_route.role'))

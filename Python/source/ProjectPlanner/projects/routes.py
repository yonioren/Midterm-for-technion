from flask import render_template, request, redirect, url_for, flash
from . import projects_bp
from ..controllers.projects import list_projects, add_new_project, edit_existing_project, delete_existing_project

# GET - display existing projects
@projects_bp.route('/')
def index():
    projects, items = list_projects()
    return render_template('projects.html',
                           projects=projects,
                           items=items)

# POST - add a new project
@projects_bp.route('/add', methods=['POST'])
def add_project():
    name = request.form['name'].strip()
    resources = {k[5:]: int(v) for k, v in request.form.items() if
                 k.startswith('item_') and k[5:].isdigit() and v and int(v) > 0}

    message = add_new_project(name, resources)

    flash(message)
    return redirect(url_for('projects.index'))

# POST - edit existing project
@projects_bp.route('/edit/<int:project_id>', methods=['POST'])
def edit_project(project_id):
    name = request.form['name'].strip()
    resources = {k[5:]: int(v) for k, v in request.form.items() if
                 k.startswith('item_') and k[5:].isdigit() and v and int(v) > 0}

    message = edit_existing_project(str(project_id),name,resources)

    flash(message)
    return redirect(url_for('projects.index'))

# POST -- delete project
@projects_bp.route('/delete/<int:project_id>', methods=['POST'])
def delete_project(project_id):
    message = delete_existing_project(str(project_id))

    flash(message)
    return redirect(url_for('projects.index'))

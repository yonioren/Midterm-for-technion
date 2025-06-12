from flask import render_template, request, redirect, url_for
from . import projects_bp
from ..models import projects, inventory_items, Project

@projects_bp.route('/')
def list_projects():
    return render_template('projects.html', projects=projects, items=inventory_items)

@projects_bp.route('/add', methods=['POST'])
def add_project():
    name = request.form['name']
    resources = {
        int(k.split('_')[1]): int(v)
        for k, v in request.form.items() if k.startswith("item_") and int(v) > 0
    }
    project = Project(name=name, resources=resources)
    projects.append(project)
    return redirect(url_for('projects.list_projects'))

@projects_bp.route('/edit/<int:project_id>', methods=['POST'])
def edit_project(project_id):
    for p in projects:
        if p.id == project_id:
            p.name = request.form['name']
            p.resources = {
                int(k.split('_')[1]): int(v)
                for k, v in request.form.items() if k.startswith("item_") and int(v) > 0
            }
            break
    return redirect(url_for('projects.list_projects'))

@projects_bp.route('/delete/<int:project_id>', methods=['POST'])
def delete_project(project_id):
    for p in projects:
        if p.id == project_id:
            projects.remove(p)
            break
    return redirect(url_for('projects.list_projects'))

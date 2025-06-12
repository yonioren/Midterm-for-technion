from flask import render_template, request, redirect, url_for, flash
from . import projects_bp
from ..models import projects, inventory_items, Project

@projects_bp.route('/')
def index():
    return render_template('projects.html', projects=projects, items=inventory_items)

@projects_bp.route('/add', methods=['POST'])
def add_project():
    name = request.form['name'].strip()

    # Check for uniqueness
    if any(p.name.lower() == name.lower() for p in projects):
        flash(f"Project '{name}' already exists.")
        return redirect(url_for('projects.index'))

    resources = {
        item.id: int(request.form.get(f'item_{item.id}', 0))
        for item in inventory_items
        if request.form.get(f'item_{item.id}') and int(request.form.get(f'item_{item.id}')) > 0
    }
    new_project = Project(name=name, resources=resources)
    projects.append(new_project)
    flash(f"Added project: '{new_project.name}'.")
    return redirect(url_for('projects.index'))

@projects_bp.route('/edit/<int:project_id>', methods=['POST'])
def edit_project(project_id):
    project = next((p for p in projects if p.id == project_id), None)
    if project:
        new_name = request.form['name'].strip()
        if new_name.lower() != project.name.lower() and any(p.name.lower() == new_name.lower() for p in projects):
            flash(f"Cannot rename project to '{new_name}'; a project with this name already exists.")
            return redirect(url_for('projects.index'))

        changes = []
        if new_name != project.name:
            changes.append(f"name: '{project.name}' → '{new_name}'")
            project.name = new_name

        new_resources = {
            item.id: int(request.form.get(f'item_{item.id}', 0))
            for item in inventory_items
            if request.form.get(f'item_{item.id}') and int(request.form.get(f'item_{item.id}')) > 0
        }

        if new_resources != project.resources:
            res_changes = []
            all_keys = set(project.resources.keys()).union(new_resources.keys())
            for k in all_keys:
                old_qty = project.resources.get(k, 0)
                new_qty = new_resources.get(k, 0)
                if old_qty != new_qty:
                    item_name = next((i.name for i in inventory_items if i.id == k), f"Item {k}")
                    res_changes.append(f"{item_name}: {old_qty} → {new_qty}")
            changes.append("resources updated: " + "; ".join(res_changes))
            project.resources = new_resources

        if changes:
            flash(f"Updated project '{project.name}': " + "; ".join(changes))
        else:
            flash(f"No changes made to project '{project.name}'.")
    return redirect(url_for('projects.index'))

@projects_bp.route('/delete/<int:project_id>', methods=['POST'])
def delete_project(project_id):
    project = next((p for p in projects if p.id == project_id), None)
    if project:
        projects.remove(project)
        flash(f"Deleted project: '{project.name}'.")
    return redirect(url_for('projects.index'))

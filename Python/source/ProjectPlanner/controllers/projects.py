from ..models.project import ProjectDB
from ..models.inventory_item import InventoryItemDB
import sys

def list_projects():
    # The order matters!
    items = InventoryItemDB.all()
    projects = ProjectDB.all()
    return projects, items

def add_new_project(name, resources_quantities):
    name = name.strip()

    projects, items = list_projects()

    # Uniqueness check
    if any(p.name.lower() == name.lower() for p in projects):
        return None, f"Project '{name}' already exists."

    new_proj = ProjectDB.add(name, resources_quantities)
    return f"Added project: '{new_proj.name}'."


def edit_existing_project(pid, name, resources):
    projects, items = list_projects()

    project = next((p for p in projects if p.id == pid), None)
    if not project:
        return "Project not found."

    new_name = name

    # Uniqueness
    if new_name.lower() != project.name.lower() and any(
            p.name.lower() == new_name.lower() for p in projects
    ):
        return f"Cannot rename project; '{new_name}' already exists."

    changes = []

    if new_name != project.name:
        changes.append(f"name: '{project.name}' → '{new_name}'")
    project.name = new_name

    new_resources = resources

    if new_resources != project.resources:
        res_changes = []
        all_keys = set(project.resources.keys()).union(new_resources.keys())
        for k in all_keys:
            old = project.resources.get(k, 0)
            new = new_resources.get(k, 0)
            if old != new:
                item_name = next((i.name for i in items if i.id == k), f"Item {k}")
                res_changes.append(f"{item_name}: {old} → {new}")

        changes.append("resources updated: " + "; ".join(res_changes))
        project.resources = new_resources

    if not changes:
        return f"No changes made to project '{project.name}'."

    # Save changes
    ProjectDB.save_all(projects)
    return f"Updated project '{project.name}': " + "; ".join(changes)

def delete_existing_project(pid):
    project = ProjectDB.get_by_id(pid)

    if not project:
        return "Project not found."
    ProjectDB.delete(pid)
    return f"Deleted project: '{project.name}'."

def project_name_taken(name):
    return ProjectDB.get_by_name(str(name)) is not None


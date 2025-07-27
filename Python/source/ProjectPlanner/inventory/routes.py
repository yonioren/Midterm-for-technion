from flask import render_template, request, redirect, url_for, flash
from . import inventory_bp
from ..models import inventory_items, projects, InventoryItem

# GET -- show all inventory
@inventory_bp.route('/')
def index():
    return render_template('inventory.html', items=inventory_items)

# POST -- add a new item
@inventory_bp.route('/add', methods=['POST'])
def add_item():
    name = request.form['name'].strip()

    # Check for uniqueness
    if any(i.name.lower() == name.lower() for i in inventory_items):
        flash(f"Item '{name}' already exists.")
        return redirect(url_for('inventory.index'))

    new_item = InventoryItem(
        name=name,
        cpu=int(request.form['cpu']),
        ram=int(request.form['ram']),
        hd=int(request.form['hd']),
        price=float(request.form['price'])
    )
    inventory_items.append(new_item)
    flash(f"Added inventory item: '{new_item.name}'.")
    return redirect(url_for('inventory.index'))

## POST - edit existing
@inventory_bp.route('/edit/<int:item_id>', methods=['POST'])
def edit_item(item_id):
    item = next((i for i in inventory_items if i.id == item_id), None)
    if item:
        new_name = request.form['name'].strip()

        # Technically possible but I will not allow changing the name to an already taken name
        if new_name.lower() != item.name.lower() and any(i.name.lower() == new_name.lower() for i in inventory_items):
            flash(f"Cannot rename item to '{new_name}'; an item with this name already exists.")
            return redirect(url_for('inventory.index'))

        # Calculate changes
        changes = []
        if item.name != new_name:
            changes.append(f"name: '{item.name}' → '{new_name}'")
            item.name = new_name
        if item.cpu != int(request.form['cpu']):
            changes.append(f"CPU: {item.cpu} → {request.form['cpu']}")
            item.cpu = int(request.form['cpu'])
        if item.ram != int(request.form['ram']):
            changes.append(f"RAM: {item.ram} → {request.form['ram']}")
            item.ram = int(request.form['ram'])
        if item.hd != int(request.form['hd']):
            changes.append(f"HD: {item.hd} → {request.form['hd']}")
            item.hd = int(request.form['hd'])
        if item.price != float(request.form['price']):
            changes.append(f"Price: ${item.price:.2f} → ${float(request.form['price']):.2f}")
            item.price = float(request.form['price'])

        # Print only the changes
        if changes:
            flash(f"Updated item '{item.name}': " + "; ".join(changes))
        else:
            flash(f"No changes made to item '{item.name}'.")
    return redirect(url_for('inventory.index'))

# POST - delete item
@inventory_bp.route('/delete/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    item = next((i for i in inventory_items if i.id == item_id), None)
    if not item:
        return redirect(url_for('inventory.index'))

    # Cannot delete an item that a project still uses otherwise people get mad
    used = any(item_id in p.resources for p in projects)
    if used:
        flash(f"Cannot delete '{item.name}'; it is used in a project.")
    else:
        inventory_items.remove(item)
        flash(f"Deleted inventory item: '{item.name}'.")
    return redirect(url_for('inventory.index'))

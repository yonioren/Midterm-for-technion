from flask import render_template, request, redirect, url_for, flash
from . import inventory_bp
from ..models import inventory_items, projects, InventoryItem

@inventory_bp.route('/')
def list_items():
    return render_template('inventory.html', items=inventory_items)

@inventory_bp.route('/add', methods=['POST'])
def add_item():
    item = InventoryItem(
        name=request.form['name'],
        cpu=int(request.form['cpu']),
        ram=int(request.form['ram']),
        hd=int(request.form['hd']),
        price=float(request.form['price'])
    )
    inventory_items.append(item)
    return redirect(url_for('inventory.list_items'))

@inventory_bp.route('/edit/<int:item_id>', methods=['POST'])
def edit_item(item_id):
    for item in inventory_items:
        if item.id == item_id:
            item.name = request.form['name']
            item.cpu = int(request.form['cpu'])
            item.ram = int(request.form['ram'])
            item.hd = int(request.form['hd'])
            item.price = float(request.form['price'])
            break
    return redirect(url_for('inventory.list_items'))

@inventory_bp.route('/delete/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    for item in inventory_items:
        if item.id == item_id:
            if any(item_id in p.resources for p in projects):
                flash("Cannot delete item in use by a project.", "error")
            else:
                inventory_items.remove(item)
            break
    return redirect(url_for('inventory.list_items'))

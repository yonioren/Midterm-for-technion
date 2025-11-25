from flask import render_template, request, redirect, url_for, flash
from . import inventory_bp
from ..controllers.inventory import list_inventory_items, add_inventory_item, edit_inventory_item, delete_inventory_item

# GET -- show all inventory
@inventory_bp.route('/')
def index():
    return render_template('inventory.html', items=list_inventory_items())

# POST -- add a new item
@inventory_bp.route('/add', methods=['POST'])
def add_item():
    message = add_inventory_item(
        name=request.form['name'].strip(),
        cpu=int(request.form['cpu']),
        ram=int(request.form['ram']),
        hd=int(request.form['hd']),
        price=float(request.form['price'])
    )

    flash(message)
    return redirect(url_for('inventory.index'))

## POST - edit existing
@inventory_bp.route('/edit/<int:item_id>', methods=['POST'])
def edit_item(item_id):
    message = edit_inventory_item(
        str(item_id),
        request.form['name'].strip(),
        int(request.form['cpu']),
        int(request.form['ram']),
        int(request.form['hd']),
        float(request.form['price'])
    )

    flash(message)
    return redirect(url_for('inventory.index'))

# POST - delete item
@inventory_bp.route('/delete/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    message = delete_inventory_item(str(item_id))

    flash(message)
    return redirect(url_for('inventory.index'))


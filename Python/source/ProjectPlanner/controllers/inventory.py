from ..models.project import ProjectDB
from ..models.inventory_item import InventoryItemDB

def list_inventory_items():
    return InventoryItemDB.all()

def add_inventory_item(name, cpu, ram, hd, price):
    items = list_inventory_items()

    # Uniqueness check
    if any(i.name.lower() == name.lower() for i in items):
        return f"Item '{name}' already exists."

    new_item = InventoryItemDB.add(name, cpu, ram, hd, price)
    return f"Added item: '{new_item.name}'."


def edit_inventory_item(iid, name, cpu, ram, hd, price):
    items = list_inventory_items()

    item = next((i for i in items if i.id == iid), None)
    if not item:
        return "Item not found."

    new_name = name

    # Uniqueness
    if new_name.lower() != item.name.lower() and any(
            i.name.lower() == new_name.lower() for i in items
    ):
        return f"Cannot rename item; '{new_name}' already exists."

    changes = []

    if new_name != item.name:
        changes.append(f"name: '{item.name}' → '{new_name}'")
        item.name = new_name
    if item.cpu != cpu:
        changes.append(f"CPU: {item.cpu} → {cpu}")
        item.cpu = cpu
    if item.ram != ram:
        changes.append(f"RAM: {item.ram} → {ram}")
        item.ram = ram
    if item.hd != hd:
        changes.append(f"HD: {item.hd} → {hd}")
        item.hd = hd
    if item.price != price:
        changes.append(f"Price: ${item.price:.2f} → ${price:.2f}")
        item.price = price

    if not changes:
        return f"No changes made to item '{item.name}'."

    # Save changes
    InventoryItemDB.save_all(items)
    return f"Updated item '{item.name}': " + "; ".join(changes)

def delete_inventory_item(iid):
    item = InventoryItemDB.get_by_id(iid)
    projects = ProjectDB.all()

    if not item:
        return "Item not found."
    if any(iid in p.resources for p in projects):
        return f"Cannot delete '{item.name}'; it used in a project"
    InventoryItemDB.delete(iid)
    return f"Deleted item: '{item.name}'."

def item_name_taken(name):
    return InventoryItemDB.get_by_name(str(name)) is not None
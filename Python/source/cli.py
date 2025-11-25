from ProjectPlanner.controllers.projects import list_projects, add_new_project, edit_existing_project, delete_existing_project, project_name_taken
from ProjectPlanner.controllers.inventory import list_inventory_items, add_inventory_item, edit_inventory_item, delete_inventory_item, item_name_taken
from ProjectPlanner.controllers.statistics import get_stats


def input_int(prompt, default=None, retry=True):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            if not retry:
                return default
            print("Please insert a valid integer.")

def input_float(prompt, default=None, retry=True):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            if not retry:
                return default
            print("Please insert a valid float.")

def input_bool(prompt, default=False, retry=True):
    prompt = prompt + " " if prompt else ""
    prompt+="(Y/n): "
    while True:
        try:
            user_input_raw = input(prompt)
            if str(user_input_raw).lower() in ['y','yes']:
                return True
            return False
        except ValueError:
            if not retry:
                return default
            prompt="(Y/n): "

### MAIN
def show_menu():
    print("\n=== MAIN MENU ===")

    ## Inventory
    print("1. Show inventory items")
    print("2. Add inventory item")
    print("3. Edit inventory item")
    print("4. Delete inventory item")

    ## Projects
    print("5. Show projects")
    print("6. Add project")
    print("7. Edit project")
    print("8. Delete project")

    ## Statistics
    print("9. Show statistics")
    print()
    print("0. Exit")

### Inventory
def show_inventory_items_cli(detailed=True):
    items = list_inventory_items()

    if not items:
        print("No inventory items found.")
        return
    for item in items:
        print(f"[{item.id}] {item.name}")
        if detailed:
            print(f" - CPU: {item.cpu}")
            print(f" - RAM: {item.ram}")
            print(f" - HD: {item.hd}")
            print(f" - Price: {item.price}$")
        print()

def add_inventory_item_cli():
    name = input("Inventory item name: ").strip()

    if item_name_taken(name):
        print("Inventory item name is already taken")
        return

    cpu = input_int(f"Quantity of CPU (int): ")
    ram = input_int(f"Amount of RAM (int): ")
    hd = input_int(f"Amount of HD disk space in GB (int): ")
    price = input_int(f"Price in $ (float): ")

    print(f"You are about to add inventory item {name} with the following resources: ")
    print(f" - CPU: {cpu}")
    print(f" - RAM: {ram}")
    print(f" - HD: {hd}")
    print(f" - Price: {price}$")
    print()

    if input_bool("Do you agree? "):
        msg = add_inventory_item(name, cpu, ram, hd, price)
    else:
        msg = "Aborting"

    print(msg)

def edit_inventory_item_cli():
    show_inventory_items_cli(detailed=False)
    print()
    iid = input_int("Inventory item ID to edit: ")

    items = list_inventory_items()
    item = next((i for i in items if i.id == iid), None)
    if not item:
        print("Inventory item not found.")
        return

    print(f"Editing item '{item.name}'")
    new_name = input(f"New name (leave blank to keep '{item.name}'): ").strip()
    cpu = input_int(f"Quantity of CPU (int) (leave blank to keep '{item.cpu}: ", default=item.cpu, retry=False)
    ram = input_int(f"Amount of RAM (int): ", default=item.ram, retry=False)
    hd = input_int(f"Amount of HD disk space in GB (int): ", default=item.hd, retry=False)
    price = input_int(f"Price in $ (float): ", default=item.price, retry=False)

    old_name_prompt = ""
    if new_name:
        old_name_prompt = f" (old name: {item.name})"
        name = new_name
    else:
        name = item.name

    print(f"You are about to edit inventory item {name + old_name_prompt} with the following resources: ")
    print(f" - CPU: {cpu}")
    print(f" - RAM: {ram}")
    print(f" - HD: {hd}")
    print(f" - Price: {price}$")
    print()

    if input_bool("Do you agree? "):
        msg = edit_inventory_item(iid, name, cpu, ram, hd, price)
    else:
        msg = "Aborting"

    print(msg)

def delete_inventory_item_cli():
    show_inventory_items_cli(detailed=False)
    print()
    iid = input_int("Inventory item ID to delete: ")

    if input_bool("Are you sure you want to delete this project? ", retry=False):
        msg = delete_inventory_item(iid)
    else:
        msg = "Aborting"

    print(msg)

### Projects
def show_projects_cli(detailed=True):
    projects, items = list_projects()

    if not projects:
        print("No projects found.")
        return
    for p in projects:
        print(f"[{p.id}] {p.name}")
        if detailed:
            for item_id, qty in p.resources.items():
                item = next((i for i in items if i.id == item_id), None)
                if item:
                    print(f" - {item.name}: {qty}")
        print()

def add_project_cli():
    name = input("Project name: ").strip()

    if project_name_taken(name):
        print("Project name is already taken")
        return

    items = list_inventory_items()

    resources = {}
    for item in items:
        qty = input_int(f"Quantity of {item.name} (0 to skip): ", 0, retry=False)
        if isinstance(qty, int) and qty > 0:
            resources[f"{item.id}"] = qty

    print(f"You are about to add project {name} with the following resources: ")
    for item_id, qty in resources.items():
        item = next((i for i in items if i.id == item_id), None)
        if item:
            print(f" - {item.name}: {qty}")

    if input_bool("Do you agree? "):
        msg = add_new_project(name, resources)
    else:
        msg = "Aborting"

    print(msg)


def edit_project_cli():
    show_projects_cli(detailed=False)
    print()
    pid = input_int("Project ID to edit: ")

    projects, items = list_projects()
    project = next((p for p in projects if p.id == pid), None)
    if not project:
        print("Project not found.")
        return

    print(f"Editing project '{project.name}'")
    new_name = input(f"New name (leave blank to keep '{project.name}'): ").strip()
    resources = {}
    for item in items:
        current = project.resources.get(item.id, 0)
        qty = input_int(f"{item.name} quantity [{current}]: ", current, retry=False)
        if isinstance(qty, int) and qty > 0:
            resources[f"{item.id}"] = qty

    old_name_prompt=""
    if new_name:
        old_name_prompt=f" (old name: {project.name})"
        name = new_name
    else:
        name = project.name

    print(f"You are about to edit project {name+old_name_prompt} with the following resources: ")
    for item_id, qty in resources.items():
        item = next((i for i in items if i.id == item_id), None)
        if item:
            print(f" - {item.name}: {qty}")

    if input_bool("Do you agree? "):
        msg = edit_existing_project(pid, name, resources)
    else:
        msg = "Aborting"

    print(msg)

def delete_project_cli():
    show_projects_cli(detailed=False)
    print()
    pid = input_int("Project ID to delete: ")

    if input_bool("Are you sure you want to delete this project? ", retry=False):
        msg = delete_existing_project(pid)
    else:
        msg = "Aborting"

    print(msg)

### Statistics
def show_statistics_cli():
    stats = get_stats()

    print("\n=== STATISTICS ===")
    for k, v in stats.items():
        print(f"{k}: {str(v)}")

    print()


def main():
    print("Welcome to the Project/Inventory CLI!")

    while True:
        show_menu()
        choice = input_int("Select an option: ")
        if choice == 1:
            show_inventory_items_cli()
        elif choice == 2:
            add_inventory_item_cli()
        elif choice == 3:
            edit_inventory_item_cli()
        elif choice == 4:
            delete_inventory_item_cli()
        elif choice == 5:
            show_projects_cli()
        elif choice == 6:
            add_project_cli()
        elif choice == 7:
            edit_project_cli()
        elif choice == 8:
            delete_project_cli()
        elif choice == 9:
            show_statistics_cli()
        elif choice == 0:
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()
# A smart iterator. NICE!
import itertools

# TODO: Move these to an actual DB!
inventory_items = []
projects = []
item_id_counter = itertools.count(1)
project_id_counter = itertools.count(1)

class InventoryItem:
    def __init__(self, name, cpu, ram, hd, price):
        self.id = next(item_id_counter) ## Not needed when DB is here
        self.name = name
        self.cpu = cpu
        self.ram = ram
        self.hd = hd
        self.price = price

class Project:
    def __init__(self, name, resources):  # {item_id: quantity}
        self.id = next(project_id_counter) ## Not needed when DB is here
        self.name = name
        self.resources = resources

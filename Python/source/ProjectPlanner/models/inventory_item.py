from .file import load_data, save_data
from itertools import count

FILE = "inventory_items.json"
DUMMY = [
    {"id": "1", "name": "DNS", "cpu": 2, "ram": 4, "hd": 30, "price": 12.0},
    {"id": "2", "name": "LDAP", "cpu": 4, "ram": 4, "hd": 50, "price": 22.0},
    {"id": "3", "name": "Active Directory", "cpu": 8, "ram": 16, "hd": 100, "price": 53.0}
]

class InventoryItem:
    def __init__(self, id, name, cpu, ram, hd, price):
        self.id = id
        self.name = name
        self.cpu = cpu
        self.ram = ram
        self.hd = hd
        self.price = price

    def to_dict(self):
        return dict(id=self.id, name=self.name, cpu=self.cpu, ram=self.ram, hd=self.hd, price=self.price)

    @staticmethod
    def from_dict(d):
        return InventoryItem(**d)


class InventoryItemDB:
    _id_counter = count(1)

    @staticmethod
    def all():
        raw = load_data(FILE, dummy=DUMMY)

        return [InventoryItem.from_dict(x) for x in raw]

    @staticmethod
    def save_all(inventory_items):
        save_data(FILE, [i.to_dict() for i in inventory_items])

    @staticmethod
    def add(name, cpu, ram, hd, price):
        inventory_items = InventoryItemDB.all()

        new_id = str(next(InventoryItemDB._id_counter))
        i = InventoryItem(new_id, name, cpu, ram, hd, price)
        inventory_items.append(i)
        InventoryItemDB.save_all(inventory_items)

        return i

    @staticmethod
    def get_by_id(iid):
        for i in InventoryItemDB.all():
            if i.id == iid:
                return i

        return None

    @staticmethod
    def get_by_name(iname):
        for i in InventoryItemDB.all():
            if i.name == iname:
                return i

        return None

    @staticmethod
    def delete(iid):
        inventory_items = [i for i in InventoryItemDB.all() if i.id != iid]

        InventoryItemDB.save_all(inventory_items)

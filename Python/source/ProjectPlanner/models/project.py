from .file import load_data, save_data
from itertools import count

FILE = "projects.json"
DUMMY = [
    {"id": "1", "name": "DNS IT", "resources": {"1": 4}}
]

class Project:
    def __init__(self, id, name, resources):
        self.id = id

        self.name = name
        self.resources = resources

    def to_dict(self):
        return dict(id=self.id, name=self.name, resources=self.resources)

    @staticmethod
    def from_dict(d):
        return Project(**d)



class ProjectDB:
    _id_counter = count(1)

    @staticmethod
    def all():
        raw = load_data(FILE, dummy=DUMMY)

        return [Project.from_dict(x) for x in raw]

    @staticmethod
    def save_all(projects):
        save_data(FILE, [p.to_dict() for p in projects])

    @staticmethod
    def add(name, resources):
        projects = ProjectDB.all()

        new_id = str(next(ProjectDB._id_counter))
        p = Project(new_id, name, resources)
        projects.append(p)
        ProjectDB.save_all(projects)

        return p

    @staticmethod
    def get_by_id(pid):
        for p in ProjectDB.all():
            if p.id == pid:
                return p

        return None

    @staticmethod
    def get_by_name(pname):
        for p in ProjectDB.all():
            if p.name.lower() == pname.lower():
                return p

        return None

    @staticmethod
    def delete(pid):
        projects = [p for p in ProjectDB.all() if p.id != pid]

        ProjectDB.save_all(projects)


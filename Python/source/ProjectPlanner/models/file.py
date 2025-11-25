import json, os, time
DB_DIR = os.path.abspath(os.path.expanduser(os.getenv("DB_DIR", "db").strip('"')))

def _path(name):
    os.makedirs(DB_DIR, exist_ok=True)

    return os.path.join(DB_DIR, name)

def load_data(name, dummy):
    path = _path(name)

    if not os.path.exists(path):
        save_data(name, dummy)
        return dummy

    return json.load(open(path))

def save_data(name, data):
    path = _path(name)

    lock = path + ".lock"
    while os.path.exists(lock):
        time.sleep(0.02)
    open(lock, "w").close()

    tmp = path + ".tmp"
    json.dump(data, open(tmp, "w"))
    os.replace(tmp, path)
    os.remove(lock)
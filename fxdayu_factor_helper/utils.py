import os

_data_root = None

def get_default_data_root():
    fxdayu_root = os.environ.get("FXDAYU_ROOT", os.path.expanduser("~/.fxdayu"))
    return  os.path.join(fxdayu_root, "data")

def get_data_root():
    global _data_root
    if _data_root is None:
        _data_root = get_default_data_root()
    return _data_root

def set_data_root(path):
    global _data_root
    _data_root = path
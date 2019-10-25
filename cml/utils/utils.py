from os import path

def script_dir():
    """Get path to directory the script resides in."""
    return path.realpath(path.join(path.dirname(__file__), '../../'))

def data_dir():
    """Get path to cm's data directory."""
    return path.realpath(path.join(path.dirname(__file__), '../../data/'))

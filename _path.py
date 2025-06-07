import pathlib

def currentPath():
    return pathlib.Path(__file__).parent.resolve()
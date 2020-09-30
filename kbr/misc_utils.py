import kbr.file_utils as file_utils

def to_list(value) -> list:
    if isinstance(value, list):
        return value

    return [ value ]

def readin_if_file(name:str) -> str:

    if os.path.isfile( name):
        name = file_utils.read(name)
    return name


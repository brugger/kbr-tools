
import os

import kbr.string_utils as string_utils


def read(filename:str) -> str:
    
    file_handle = open(filename, 'r')
    content = file_handle.read()
    file_handle.close()

    return content


def find_all(name:str, path:str='.') -> []:
    result = []
    for root, dirs, files in os.walk(path):
        if name in files:
            result.append(os.path.join(root, name))
    return result


def find_first(name:str, path:str=".") -> str:
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

    return None


def write(filename:str, data:str) -> None:
    with open(filename, 'w') as outfile:
        outfile.write(data)
        outfile.close()

    return None

def size(filename:str, readable:bool=True) -> str:
    st = os.stat(filename)

    if readable:
        return string_utils.readable_bytes( st.st_size )
    else:
        return st.st_size


def changed(filename:str):
    st = os.stat(filename)
    return st.st_mtime
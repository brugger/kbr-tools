
import os
import re

import kbr.string_utils as string_utils


def read(filename:str) -> str:
    
    file_handle = open(filename, 'r')
    content = file_handle.read()
    file_handle.close()

    return content


def find_all(name:str, path:str='.') -> list:
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


def find_updir(name:str, path:str=".") -> str:
    path = os.path.abspath(path)
    if os.path.isfile( f"{path}/{name}"):
        return f"{path}/{name}"
    elif path == "/":
        return None
    else:
        return find_updir( name, f"{path}/../")


def find_pattern(pattern:str, path:str=".") -> list:

    if pattern.startswith("*"):
        pattern = f".{pattern}"

    pattern = re.compile(f"{pattern}$")

    files = []
    for root, dirs, filenames in os.walk(path):
        for filename in filenames:
            if pattern.search(filename):
                files.append(os.path.join(root, filename))
  
    return files


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


def exists(filename:str) -> bool:
    return os.path.isfile( filename )


def delete(*files) -> None:
    for f in files:
        if f is not None and os.path.isfile( f ):
            os.remove(f)



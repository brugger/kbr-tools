
import os


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

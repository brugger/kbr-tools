import os
import kbr.file_utils as file_utils
import typing

def to_list(value) -> list:
    if isinstance(value, list):
        return value

    return [ value ]

def readin_if_file(name:str) -> str:

    if os.path.isfile( name):
        return file_utils.read(name)

    return None

def pop_value(key:str, container:typing.Union[dict,list]) -> typing.Tuple[any, typing.Union[dict, list]]:

    value = None
    if isinstance(container, dict):
        if key in container:
            value = container[key]
            del container[key]

        return value, container


    if isinstance(container, list):
        if key in container:
            value = key
            container.remove(key)

        return value, container


    raise TypeError('function accepts either a list or a dictionary as the container')        




import os


def mkdirs(dirs:list) -> None:
    for d in dirs:
        os.mkdir( d )



def file_path(filename:str=None) -> str:
    if filename is None:
        filename = __file__
        
    return os.path.realpath(__file__) 


def file_dir(filename:str=None) -> str:
    return os.path.dirname(file_path(filename))

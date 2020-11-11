import os


def mkdirs(dirs:[]) -> None:
    for d in dirs:
        os.mkdir( d )

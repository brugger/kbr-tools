import hashlib



def file(filename:str) -> str:
    return hashlib.md5(open('filename.exe','rb').read()).hexdigest()

def file_check(filename:str, md5sum:str) -> bool:

    file_md5 = file(filename)
    return file_md5 == md5sum



def string( string:str) -> str:
    return hashlib.md5(string).hexdigest()


def string_check(string:str, md5sum:str) -> bool:

    file_md5 = string(filename)
    return file_md5 == md5sum


def readin_file( filename:str) -> str:
    
    file_handle = open(filename, 'r')
    content = file_handle.read()
    file_handle.close()

    return content

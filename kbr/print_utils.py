import sys 

def stderr(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
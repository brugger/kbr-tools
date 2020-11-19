import time

memcache = {}

def set(key:str, value:any, expire=0):
    memcache[ key ] = {'value':value, 'expire': 0}
    if expire:
        memcache[key]['expire'] = time.time() + expire

def get(key:str) -> any:
    value =  memcache.get(key, None)
    if value:
        if value['expire'] == 0:
            return value['value']
        elif  value['expire'] >= time.time():
            return value['value']

    return None

def delete(key:str):
    del memcache[key]

def exists(key:str) -> bool:
    value =  memcache.get(key, None)
    if value:
        if value['expire'] == 0:
            True
        elif  value['expire'] >= time.time():
            return True

    return False

def flush():
    global memcache
    memcache = {}


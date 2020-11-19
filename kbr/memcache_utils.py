from pymemcache.client import base

memcache = None



def connect(host="localhost", port=11211, namespace:str='' ):
    global memcache
    namespace = bytes(str(namespace), 'utf-8')
    memcache = base.Client(( host, port), key_prefix=namespace, )

def disconnect():
    if memcache is not None:
        memcache.quit()

def set(key:str, value:any, expire=0):
        memcache.set(key, value, expire)

def get(key:str) -> any:
    return memcache.get(key)

def delete(key:str):
    return memcache.delete(key)

def exists(key:str) -> bool:
    result = memcache.get(key)

    if result is not None:
        return True

    return False

def flush():
    memcache.flush_all()


import sys

import importlib



def reload_module(name:str):

    print(f'trying to (re)load module : {name}', flush=True)
    if name in sys.modules:
        mod_obj = importlib.import_module(name)
        importlib.reload(mod_obj)
    else:
        mod_obj = importlib.import_module(name)


    return mod_obj

def get_function(mod_obj, func_name):
    return getattr(mod_obj, func_name)

def call_function(mod_obj, func_name, *args, **kwargs):
    return getattr(mod_obj, func_name)(*args, **kwargs)



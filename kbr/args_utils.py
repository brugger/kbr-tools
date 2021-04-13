import argparse
import os
import sys

def basic_parser():
    parser = argparse.ArgumentParser(description='cli for user management')
    parser.add_argument('-c', '--config', default="api.json", help="config file, can be overridden by parameters")
    parser.add_argument('-d', '--database', default=None)
    subparsers = parser.add_subparsers(dest='subparser')


    return parser.parse_args()


def count(required:int, count:int, name:str=None, msg:str=None):
    if ( required != count):
        if msg is None:
            msg = "command requires {required} argument(s)".format( required=required)
            if name is not None:
                msg = "{} {}".format( name, msg)

        print(msg)
        sys.exit()

def min_count(required:int, count:int, name:str=None, msg:str=None):
    if ( required > count):
        if msg is None:
            msg = "command requires {required} or more argument(s)".format( required=required )
            if name is not None:
                msg = "{} {}".format( name, msg)

        print(msg)
        sys.exit()

def count_subcommand(required:int, count:int, name:str=None, msg:str=None):

    msg = "command requires a subcommand (run with help)"

    if name is not None:
        msg = "{} {}".format( name, msg)

    return count(required=required, count=count, name=name, msg=msg)

def min_count_subcommand(required:int, count:int, name:str=None, msg:str=None):
    msg = "command requires a subcommand (run with help)"

    if name is not None:
        msg = "{} {}".format( name, msg)

    return min_count(required=required, count=count, name=name, msg=msg)


def valid_command(command:int, commands:int, msg:str=None):
    if command not in commands:
        print("Invalid command name: '{}', allowed commands are {}".format( command, ", ".join(commands)))
        sys.exit()

def get_or_default(args:list, default:any):
    if len( args):
        return args.pop(0)
    return default

def get_or_fail(args:list, msg:str):
    if len( args):
        return args.pop(0)
    print(msg)
    sys.exit()

def get_env_var(name:str, default:str=None) -> str:
    return os.getenv(name, default)


def group_args(args) -> {}:
    ''' args like i:input1 i:input2 o:output'''
    res = {'':[]}
    for arg in args:
        m = re.match(r'(\w):(\w+)', arg)
        if m is not None:
            k, v = m.group(1), m.group(2)
            if k not in res:
                res[ k ] = []
            res[ k ].append(v)
        else:
            res[ 'rest' ].append(v)
            
    return res

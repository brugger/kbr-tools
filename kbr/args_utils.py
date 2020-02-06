import argparse
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
        return args[0]
    return default


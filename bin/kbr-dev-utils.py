#!/usr/bin/env python3
#
#
#
#
# Kim Brugger (03 Apr 2019), contact: kim@brugger.dk

import sys
import pprint
pp = pprint.PrettyPrinter(indent=4)
import json
import argparse
import kbr.args_utils as args_utils
import kbr.version_utils as version_utils


def version_command(args) -> None:

    commands = ['bump', 'info', 'help']
    if len( args.command) == 0:
        args.command.append( 'help')

    command = args.command.pop( 0 )
    args_utils.valid_command(command, commands)

    if command == 'bump':
        args_utils.count(1, len(args.command), msg="version bump requires; major/minor/patch")
        bump = args.command.pop( 0 )
        args_utils.valid_command(bump, ['major', 'minor','patch'])
        version_utils.bump_version( bump )
    elif command == 'info':
        version_utils.info()
    elif command == 'set':
        version = args.command.pop( 0 )
        version_utils.set( version )
    else:
        print("version sub-commands: {}".format(", ".join(commands)))
        sys.exit()




def main():


    parser = argparse.ArgumentParser(description='Dev utils')
    commands = ["version"]
    parser.add_argument('command', nargs='+', help="{}".format(",".join(commands)))

    args = parser.parse_args()
    # hardcoded for now.

    command = args.command.pop(0)
    if command not in commands:
        parser.print_help()

    if command == 'version':
        version_command(args)
    else:
        print("Unknown command: {} are allowed.".format(string_utils.comma_sep( commands )))
        sys.exit( 1 )

if __name__ == "__main__":
    main()
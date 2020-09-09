#!/usr/bin/env python3
""" 
 
 
 
 Kim Brugger (23 Jan 2019), contact: kim@brugger.dk
"""

import sys
import pprint
pp = pprint.PrettyPrinter(indent=4)

import argparse
import subprocess
import shlex
import time

import psutil

sys.path.append(".")

import kbr.config_utils as config_utils
import kbr.json_utils as json_utils

# python3+ is broken on centos 7, so add the /usr/local/paths by hand
sys.path.append("/usr/local/lib/python{}.{}/site-packages/".format( sys.version_info.major, sys.version_info.minor))
sys.path.append("/usr/local/lib64/python{}.{}/site-packages/".format( sys.version_info.major, sys.version_info.minor))



def find_procs_by_name(name):
    "Return a list of processes matching 'name'."
    ls = []
    for p in psutil.process_iter(attrs=['name', 'cmdline']):
#        print( p.info['cmdline'] )
        if p.info['name'] == name:
            ls.append(p)
        for arg in p.info['cmdline']:
            if name in arg:
                ls.append(p)
                break

    return ls


def write_example_config():
    data = [['command-name', 'command', 'count'], ['command-name-2', 'command-2', 'count-2']]
    filename = "daemon_check.json"
    json_utils.write( filename, data )
    print( f"Example config file written to {filename}")



def readin_config(config):
    return json_utils.read(config)

def main():
    """ main loop

    Args:
      None
    
    Returns:
      None
    
    Raises: 
      None
    """

    checks = []

    parser = argparse.ArgumentParser(description='Daemon checker, if not running re-start it ')

    parser.add_argument('-n', '--name',     help="Name to check for")
    parser.add_argument('-c', '--command',  help="command to run if name is not found")
    parser.add_argument('-N', '--number', type=int, default=1, help="number of processes to be running")
    parser.add_argument('-C', '--config',  help="json file for multiple processes")
    parser.add_argument('-X', '--example-config', action="store_true", default=False,   help="creates an example config file")
    parser.add_argument('-s', '--sleep', type=int, default=0, help="to have it run continually set sleep")
    parser.add_argument('-d', '--dry-run', action="store_true", default=False,   help="print changes")
    parser.add_argument('-v', '--verbose', action="store_true", default=False,   help="verbose logging")


    args = parser.parse_args()
    sleep = args.sleep

    if args.example_config:
        write_example_config()
        sys.exit()
    elif args.config is not None:
        checks = readin_config( args.config )
    elif args.command is not None or args.name is not None:
        if args.command is None or args.name is None:
            print("Error: argument missing -c<ommand> -n<ame> -N[number of proceses]")
            sys.exit( -1 )

        checks.append( [args.name, args.command, args.number])
    else:
        parser.print_usage()
        sys.exit( 1 )


    while True:
        for check in checks:
            name, command, number = check
            number = int( number )
            ls = find_procs_by_name( name )
            running = len( ls )
            if args.verbose:
                print(f"{running} processes match {name}")
            if ( running < number ):
                for _ in range(0, number - running ):
#                    command = shlex.split( command )
                    if args.dry_run:
                        print(command)
                    else:
                        subprocess.Popen(command, shell=True)
        if sleep == 0:
            break

        time.sleep( sleep )



if __name__ == '__main__':
    main()

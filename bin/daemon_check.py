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

# python3+ is broken on centos 7, so add the /usr/local/paths by hand
sys.path.append("/usr/local/lib/python{}.{}/site-packages/".format( sys.version_info.major, sys.version_info.minor))
sys.path.append("/usr/local/lib64/python{}.{}/site-packages/".format( sys.version_info.major, sys.version_info.minor))

import psutil

def find_procs_by_name(name):
    "Return a list of processes matching 'name'."
    ls = []
    for p in psutil.process_iter(attrs=['name']):
        if p.info['name'] == name:
            ls.append(p)
    return ls

def main():
    """ main loop

    Args:
      None
    
    Returns:
      None
    
    Raises: 
      None
    """

    parser = argparse.ArgumentParser(description='Daemon checker, if not running re-start it ')

    parser.add_argument('-n', '--name',     required=True, help="Name to check for")
    parser.add_argument('-c', '--command',  required=True,help="command to run if name is not found")
    parser.add_argument('-N', '--number',  required=False, default=1,help="number of processes to be running")


    args = parser.parse_args()
    args.number = int( args.number )

    ls = find_procs_by_name( args.name )
    running = len( ls )
    if ( running < args.number ):
        for _ in range(0, args.number - running ):
            subprocess.Popen(shlex.split( args.command ), shell=True)
    


if __name__ == '__main__':
    main()

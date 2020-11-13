#!/usr/bin/env python3
""" 
 
 
 
 Kim Brugger (23 Jan 2019), contact: kim@brugger.dk
"""
import os
import sys
import pprint
pp = pprint.PrettyPrinter(indent=4)

import argparse
import subprocess
import tabulate
import time
import datetime

import psutil

sys.path.append(".")

import kbr.log_utils as logger
import kbr.json_utils as json_utils
import kbr.version_utils as version_utils
import kbr.daemon_utils as daemon_utils

# python3+ is broken on centos 7, so add the /usr/local/paths by hand
sys.path.append("/usr/local/lib/python{}.{}/site-packages/".format( sys.version_info.major, sys.version_info.minor))
sys.path.append("/usr/local/lib64/python{}.{}/site-packages/".format( sys.version_info.major, sys.version_info.minor))

version = version_utils.as_string('kbr')


def find_procs_by_name(name):
    "Return a list of processes matching 'name'."
    ls = []
    for p in psutil.process_iter(attrs=['name', 'cmdline']):
#        logger.debug( p.info['cmdline'] )
        if p.info['name'] == name:
            ls.append(p)
        else:
#            print("--", p.info['cmdline'][:2])
            for arg in p.info['cmdline'][:2]:
                if name in arg:
                    ls.append(p)
                    break

    return ls


def write_example_config():
    data = [['command-name', 'command', 'count'], ['command-name-2', 'command-2', 'count-2']]
    filename = "jobs.json"
    json_utils.write( filename, data )
    print( f"Example config file written to {filename}")
    sys.exit()



def readin_config(config):
    return json_utils.read(config)


def kill_program(name, kill=True, list=False, verbose=False):
    ls = find_procs_by_name( name )

    if list:
        print(f"Found {len(ls)} processes matching '{name}'" )
#        print( ls )

        if verbose >3 and len(ls):
#            print( ls )
            v = []
            for l in ls:
                print( l.status())
                started = datetime.datetime.fromtimestamp(l.create_time()).strftime("%Y-%m-%d %H:%M:%S")
                v.append([l.pid, l.name(), l.status(), started])

            print( tabulate.tabulate( v , tablefmt='psql', headers=['pid', 'name', 'status', 'started']))
    else:
        logger.info( f"Found {len(ls)} processes matching '{name}'" )

    if kill:
        for p in ls:
            os.kill(p.pid, 9)


class Daemon( daemon_utils.Daemon ):
    def run(self) -> None:
        sys.stderr.write("running!\n")
        sys.stderr.write(f"Working dir {os.getcwd()}")
#        sys.exit()
#        try:
        while True:
            if args.config is not None:
                checks = readin_config( args.config )
                args.checks = checks

            for check in args.checks:
                name, command, number = check
                number = int( number )
                ls = find_procs_by_name( name )
                running = len( ls )

                logger.debug(f"{running} processes match {name}")
                if ( running < number ):
                    for _ in range(0, number - running ):
                        if args.dry_run:
                            print(command)
                        else:
                            logger.info(f"restarting {name}")
                            subprocess.Popen(command, shell=True)
            if args.sleep == 0:
                break

            time.sleep( args.sleep )

#        except KeyboardInterrupt:
#            logger.info("killed by the keyboard")



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

    parser = argparse.ArgumentParser(description='job manager, if not running re-start it ')

    parser.add_argument('-n',  '--name',     help="Name to check for")
    parser.add_argument('-c',  '--command',  help="command to run if name is not found")
    parser.add_argument('-N',  '--number', type=int, default=1, help="number of processes to be running")
    parser.add_argument('-C',  '--config',  help="json file for multiple processes")
    parser.add_argument('-X',  '--example-config', action="store_true", default=False,   help="creates an example config file")
    parser.add_argument('-sl',  '--sleep', type=int, default=0, help="to have it run continually set sleep")
    parser.add_argument('-d',  '--dry-run', action="store_true", default=False,   help="print changes")
    parser.add_argument('-l',  '--logfile', default=None, help="Logfile to write to, default is stdout")
    parser.add_argument('-v',  '--verbose', default=3, action="count", help="Increase the verbosity of logging output")
    parser.add_argument('-k',  '--kill',   type=str,  help="programs to kill")
    parser.add_argument('-K',  '--kill-all',   type=str,  help="kill all programs in the config file")
    parser.add_argument('-S',  '--status-all', type=str, help="Status for programs in config file")
    parser.add_argument('-s', '--status', type=str, help="Status count for program by name")
    parser.add_argument('--daemon-start',  default=False, action="store_true", help="start in daemon mode")
    parser.add_argument('--daemon-stop',  default=False, action="store_true", help="stop daemon")
    parser.add_argument('--daemon-restart',  default=False, action="store_true", help="restart daemon")


    global args
    args = parser.parse_args()

    if args.logfile:
        logger.init(name='job-manager', log_file=args.logfile)
    else:
        logger.init(name='job-manager', colour=True)
    logger.set_log_level(args.verbose)

    logger.info(f"start up {version}")

    if args.kill:
        kill_program( args.kill)
        sys.exit()

    if args.status:
        kill_program( args.status, kill=False, list=True, verbose=args.verbose)
        sys.exit()


    if args.kill_all is not None:
        checks = readin_config( args.kill_all )
        for check in checks:
            kill_program(check[0])
        sys.exit()

    if args.status_all is not None:
        checks = readin_config( args.status_all )
        for check in checks:
            kill_program(check[0], kill=False, list=True, verbose=args.verbose)
        sys.exit()

    daemon = Daemon("kbr-job-manager.pid")

    if args.daemon_stop:
        daemon.stop()
        sys.exit()

    if args.example_config:
        write_example_config()
        sys.exit()
    elif args.config is not None:
        checks = readin_config( args.config )
    elif args.command is not None or args.name is not None:
        if args.command is None or args.name is None:
            logger.error("Error: argument missing -c<ommand> -n<ame> -N[number of proceses]")
            sys.exit( -1 )

        checks.append( [args.name, args.command, args.number])
    else:
        parser.print_usage()
        sys.exit( 1 )

    args.checks = checks

    if args.daemon_start:
        if args.sleep == 0:
            args.sleep = 15
        daemon.start()
    elif args.daemon_restart:
        if args.sleep == 0:
            args.sleep = 15
        daemon.restart()
    else:
        daemon.run()



if __name__ == '__main__':
    main()

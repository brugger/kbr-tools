#!/usr/bin/env python3
"""



 Kim Brugger (25 Sep 2020), contact: kim@brugger.dk
"""
import socket
import argparse
import sys
import re
import tabulate
import requests

def get_host_name() -> str:
    return socket.getfqdn()

def get_state(service) -> int:

    r = requests.get(service)


    return {'code':r.status_code, 'response_time':r.elapsed.total_seconds()}


def main():
    parser = argparse.ArgumentParser(description='systemd service status reporter')

    parser.add_argument('-t', '--telegraf', default=False, action="store_true",    help="telegraf compatible format")
    parser.add_argument('-j', '--json', default=False, action="store_true",    help="telegraf compatible format")
    parser.add_argument('-n', '--name',  help="service name (otherwise hostname)")
    parser.add_argument('services', nargs='*', help="service(s) to check")

    args = parser.parse_args()


    if len(args.services) == 0:
        print("No service(s) provided to check!")
        sys.exit(1)

    if len(args.services) >1 and args.name is not None:
        print("Cannot substitute service name when probing multiple services")
        sys.exit(1)


    statuses = []

    for service in args.services:
        status = get_state(service)
        service =re.sub(r'^.*?//', '', service)
        service =re.sub(r'(.*?)/.*$', r'\1', service)
        if args.telegraf:
            line = f"service,service={service} status_code={status['code']},response_time={status['response_time']}"
            print( line )
        else:
            statuses.append( status )


    if args.json:
        print(json.dumps( statuses))
    elif not args.telegraf:
        print(tabulate.tabulate( statuses, headers={'status_code': 'code'}, tablefmt='psql'))



if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""



 Kim Brugger (25 Sep 2020), contact: kim@brugger.dk
"""
import subprocess
import argparse
import shlex
import json
import datetime

states = {'active': 1,
          'inactive': 2,
          'activating': 3,
          'deactivating': 4,
          'failed': 5,
          'not-found': 6,
          'dead': 7,}


def get_state(service_name) -> int:
    cmd = f"systemctl show --no-page {service_name}"
    p = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE) # NOQA
    stdout, stderr = p.communicate()
    stdout = stdout.decode('utf-8')
    stderr = stderr.decode('utf-8')
    res = {'name': service_name}
    if stderr:
        res['status':'status-error']
        return res

    for line in str(stdout).split("\n"):
        if "=" not in line:
            continue

        key, value = line.split("=",1)
        if key == 'ActiveState' and 'status' not in res:
            res['status'] = value
        if key == 'LoadState' and value == 'not-found':
            res['status'] = "not-found"
        if key == 'ExecMainStartTimestamp':
            ts = datetime.datetime.strptime(value, "%a %Y-%m-%d %H:%M:%S %Z")
            now =  datetime.datetime.now()

            res['uptime'] = (now - ts).total_seconds()


    res[ "status_code" ] = states[ res['status']]

    return res


def main():
    parser = argparse.ArgumentParser(description='systemd service status reporter')

    parser.add_argument('-t', '--telegraf', default=False, action="store_true",    help="telegraf compatible format")
    parser.add_argument('-j', '--json', default=False, action="store_true",    help="telegraf compatible format")
    parser.add_argument('services', nargs='+', help="service(s) to check")
    args = parser.parse_args()

    statuses = []

    for service in args.services:
        status = get_state(service)
        if args.telegraf:
            line = f"service,name={service} status={status['status']},status_code={status['status_code']}"
            if 'uptime' in status:
                line += f",uptime={status['uptime']}"
            print( line )

        elif args.json:
            statuses.append( status )

        else:

            line = f"{service:20s} {status['status_code']}/{status['status']:15}"
            if 'uptime' in status:
                line += f" {status['uptime']}s"
            print( line )


    if args.json:
        print(json.dumps( statuses))




if __name__ == "__main__":
    main()
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

import kbr.mq_utils as mq_util
import kbr.run_utils as run_utils


def callback(ch, method, properties, body):

    try:
        cmd_job_info = json.loads(body)
        if "cmd" not in cmd_job_info:
            raise Exception("Invalid message")
        # prologue - handle preparation for running job
        
        # run job
        exec_info = run_utils.launch_cmd(cmd_job_info["cmd"])
        
        # epilogue - handle execution output and cleanup
        print("exit code: %s" % exec_info.p_status)
        print("std out: %s" % exec_info.stdout)
        print("std error: %s" % exec_info.stderr)
        
        
    except Exception as ex:
        print(ex)
        # acknowledge message as handled
    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():

    parser = argparse.ArgumentParser(description='consumes a mq ')

    parser.add_argument('-u', '--uri',      default='localhost/cbu', help="uri to connect to")
    parser.add_argument('-e', '--exchange', default='default',       help="exchange to use")
    parser.add_argument('-q', '--queue',    default='default',       help="queue to pull from")
    args = parser.parse_args()

    pp.pprint( args)
    
    
    mq = mq_util.Mq()
    mq.connect(uri=args.uri, exchange=args.exchange)
    mq.consume(route=args.queue, callback=callback)

if __name__ == "__main__":
    main()
    

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

import kbr.mq_utils as mq_utils

def main():
    parser = argparse.ArgumentParser(description='consumes a mq ')

    parser.add_argument('-u', '--uri',      default='localhost/cbu', help="uri to connect to")
    parser.add_argument('-e', '--exchange', default='default',       help="exchange to use")
    parser.add_argument('-q', '--queue',    default='default',       help="queue to pull from")
    args = parser.parse_args()

    pp.pprint( args)
    
    
    mq = mq_utils.Mq()
    mq.connect(uri=args.uri, exchange=args.exchange)
    for i in range( 1, 101):
        mq.publish(route=args.queue, body=json.dumps({'cmd':'date'}))


if __name__ == "__main__":
    main()
    

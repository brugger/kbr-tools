#!/usr/bin/env python3

import os
import re
import argparse

import kbr.email_utils as email_utils
import kbr.file_utils as file_utils


def readin_if_file(name:str) -> str:

    if os.path.isfile( name):
        name = file_utils.read( name )
    return name




def main():
    parser = argparse.ArgumentParser(description='emailer tool')
    parser.add_argument('-t', '--to',      required=True, help="who to send to, comma separated ")
    parser.add_argument('-f', '--sender',    required=True, help="From address")
    parser.add_argument('-s', '--subject', required=True, help="subject")
    parser.add_argument('-b', '--body',    required=True, help="queue to pull from")
    parser.add_argument('--cc',            default='',    help="list of adresses to cc (comma separated)")
    parser.add_argument('--bcc',           default='',    help="list of adresses to bcc (comma separated)")

    parser.add_argument('--max-recipients', default=None, help='Max number of recipients')

    parser.add_argument('--smtp',          default='smtp.uib.no',  help="SMTP host to use")
    parser.add_argument('--smtp-port',     default='25',           help="SMTP port")
    parser.add_argument('--smtp-user',     default=None,           help="SMTP username")
    parser.add_argument('--smtp-password', default=None,           help="SMTP password")

    args = parser.parse_args()

    email_utils.SMTP_SERVER   = args.smtp
    email_utils.SMTP_PORT     = args.smtp_port
    email_utils.SMTP_USERNAME = args.smtp_user
    email_utils.SMTP_PASSWORD = args.smtp_password

    args.body = readin_if_file( args.body )

    args.to = readin_if_file( args.to )
    args.to = re.sub("\n", ",", args.to)

    args.cc = re.sub("\n", ",", args.cc)
    args.cc = readin_if_file( args.cc )

    args.bcc = readin_if_file( args.bcc )
    args.bcc = re.sub("\n", ",", args.bcc)

    email_utils.send_email(sender=args.sender, recipients=args.to.split(','), subject=args.subject, body=args.body, cc=args.cc.split(','), bcc=args.bcc.split(','))



if __name__ == '__main__':
    main()

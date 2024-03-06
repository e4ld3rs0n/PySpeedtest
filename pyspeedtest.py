#!/usr/bin/env python3

import argparse, speedtest, os.path

print_header = False

parser=argparse.ArgumentParser(
    usage='%(prog)s [options] -o <output file>',
    description="Internet speed tester using speedtest.net API.",
    epilog='Install the speedtest-cli package before use.'
    )

parser.add_argument(
    '-o', '--output', 
    help='File where to record the readings', 
    required=True
    )

parser.add_argument(
    '-f', '--format',
    choices={"csv", "md", "txt"},
    help='Specify an output format (default is CSV)'
)

parser.add_argument(
    '-s', '--separator',
    default=';',
    help='Specify an alternative separator character'
)

args=parser.parse_args()

if(not os.path.isfile(args.output)):
    print_header = True

with open(args.output, '+a') as logfile:
    if(print_header):
        print('PRINT HEADER')
    print('DO TEST')
    print('WRITE RESULTS')

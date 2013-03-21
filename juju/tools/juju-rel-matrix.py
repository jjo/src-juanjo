#!/usr/bin/python
## Author: JuanJo Ciarlante <jjo@canonical.com>
## Copyright 2013, Canonical Ltd.
## License: GPLv3
##
# pylint: disable=C0103,W0142
# vim: sw=4 ts=4 et ai

"""
Print a matrix relationnames, with servicenames by columns, rows
where each cell is filled by their relation(s) name.
Uses "juju status" output as input file ('-' for stdin)

Useful cmdline:
  juju status | %(prog)s - | column -t |less -SX
  juju status | %(prog)s -x nrpe -
  juju status | %(prog)s -i 'haprox|apache|app' -x nrpe -
"""

import yaml
import sys
from argparse import ArgumentParser, RawDescriptionHelpFormatter
import re

def get_common_prefix(words):
    "Get common prefix from words list"
    zip_words = zip(*words)
    common_chars = [c[0] for c in zip_words if c == (c[0],)*len(c)]
    return "".join(common_chars)

p = ArgumentParser(description='Juju relation matrix: %(prog)s filename'
                               '|column -t|less -SX',
                   epilog=__doc__, formatter_class=RawDescriptionHelpFormatter)
p.add_argument('file', type=str, nargs=1,
               help='file with "juju status" output, or "-" for stdin')
p.add_argument('-x', '--exclude', type=str, action='store',
               help='exclude services that match this string regex, eg: '
                    '"apache|haproxy"')
p.add_argument('-i', '--include', type=str, action='store',
               help='exclude services which have this string, eg.: "nrpe"')
p.add_argument('-s', '--separator', type=str, action='store', default='\t',
               help='output field separator, default: TAB')
p.add_argument('-r', '--rel-separator', type=str, action='store', default=',',
               help='same service pair relation separator (rare), default: ","')
p.add_argument('-f', '--full-name', action='store_true',
               help='show full service names, vs stripping common prefix')
args = p.parse_args()

if args.file[0] == '-':
    input_file = sys.stdin
else:
    input_file = open(args.file[0])

JUJU_STATUS = yaml.load(input_file)
if not JUJU_STATUS:
    print >> sys.stderr, "ERROR: stdin doesn't parse as YAML"
    sys.exit(1)

SERVICES = JUJU_STATUS.get('services', None)
if not SERVICES:
    print >> sys.stderr, "ERROR: no juju services found from {}".format(
        args.file)
    sys.exit(1)

if args.full_name:
    PREFIX = ''
else:
    PREFIX = get_common_prefix(SERVICES.keys())

if args.exclude:
    exclude_re = re.compile('.*({}).*'.format(args.exclude))
    SERVICES = dict([x for x in SERVICES.iteritems() 
                     if not exclude_re.match(x[0])])
if args.include:
    include_re = re.compile('.*({}).*'.format(args.include))
    SERVICES = dict([x for x in SERVICES.iteritems() 
                     if include_re.match(x[0])])

## header: services by column
print '{}X{}'.format(PREFIX, args.separator), '{}'.format(
        args.separator).join(sorted([x[len(PREFIX):] for x in SERVICES.keys()]))
## for each service, show the relation against service in column
for service_row in sorted(SERVICES.keys()):
    ## 1st column: service name
    print "{}{}".format(service_row[len(PREFIX):], args.separator),
    for service_col, service_col_dict in sorted(SERVICES.iteritems()):
        rel_output = []
        for rel_name in service_col_dict['relations']:
            if service_row in service_col_dict['relations'][rel_name]:
                rel_output.append(rel_name)
        if not rel_output:
            rel_output.append('-')
        print "{}{}".format(args.rel_separator.join(rel_output), 
                            args.separator),
    print

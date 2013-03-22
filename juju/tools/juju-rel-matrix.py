#!/usr/bin/env python
## Author: JuanJo Ciarlante <jjo@canonical.com>
## Copyright (C) 2013, Canonical Ltd.
## License: GPLv3
##
# vim: sw=4 ts=4 et ai
# pylint: disable=C0103,W0142

"""
Print a matrix relationnames, with servicenames by columns, rows
where each cell is filled by their relation(s) name.
Uses "juju status" output as input file ('-' for stdin)

Useful cmdline:
  juju status | %(prog)s - | less -SX
  juju status | %(prog)s -x nrpe -
  juju status | %(prog)s -i 'haprox|apache|app' -x nrpe -
"""

import yaml
import sys
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from subprocess import Popen, PIPE
import re


def get_common_prefix(words):
    "Get common prefix from words list"
    zip_words = zip(*words)
    common_chars = [c[0] for c in zip_words if c == (c[0],) * len(c)]
    return "".join(common_chars)


def print_relations_matrix(juju_services, args):
    "Print service-x-service relations matrix"
    if args.full_name:
        prefix = ''
    else:
        prefix = get_common_prefix(juju_services.keys())

    if args.raw:
        out = sys.stdout
        pipe = None
    else:
        pipe = Popen(['column', '-t'], stdin=PIPE)
        out = pipe.stdin

    if args.exclude:
        exclude_re = re.compile('.*({}).*'.format(args.exclude))
        juju_services = dict([x for x in juju_services.iteritems()
                         if not exclude_re.match(x[0])])
    if args.include:
        include_re = re.compile('.*({}).*'.format(args.include))
        juju_services = dict([x for x in juju_services.iteritems()
                         if include_re.match(x[0])])

    ## header: services by column
    print >> out, '{}X{}'.format(prefix, args.separator), \
          '{}'.format(args.separator).join(
                sorted([x[len(prefix):] for x in juju_services.keys()]))
    ## for each service, show the relation against service in column
    for service_row in sorted(juju_services.keys()):
        ## 1st column: service name
        print >> out, "{}{}".format(service_row[len(prefix):], args.separator),
        for _svc_col, service_col_dict in sorted(juju_services.iteritems()):
            rel_output = []
            for rel_name in service_col_dict['relations']:
                if service_row in service_col_dict['relations'][rel_name]:
                    rel_output.append(rel_name)
            if not rel_output:
                rel_output.append('-')
            print >> out, "{}{}".format(args.rel_separator.join(rel_output),
                                args.separator),
        print >> out
    if pipe:
        pipe.communicate()

p = ArgumentParser(description='Juju relation matrix: %(prog)s filename'
                               '|column -t|less -SX',
                   epilog=__doc__, formatter_class=RawDescriptionHelpFormatter)
p.add_argument('files', type=str, nargs='+',
               help='file with "juju status" output, or "-" for stdin')
p.add_argument('-x', '--exclude', type=str, action='store',
               help='exclude services that match this string regex, eg: '
                    '"apache|haproxy"')
p.add_argument('-i', '--include', type=str, action='store',
               help='exclude services which have this string, eg.: "nrpe"')
p.add_argument('-s', '--separator', type=str, action='store', default='\t',
               help='output field separator, default: TAB')
p.add_argument('-r', '--rel-separator', type=str, action='store', default=',',
               help='same service pair relation separator, default: ","')
p.add_argument('-f', '--full-name', action='store_true',
               help='show full service names, vs stripping common prefix')
p.add_argument('--raw', action='store_true',
               help="raw ouput, don't pipe thru 'column -t'")
cmd_args = p.parse_args()

for filename in cmd_args.files:
    if filename == '-':
        input_file = sys.stdin
    else:
        input_file = open(filename)

    juju_status = yaml.load(input_file)
    if not juju_status:
        print >> sys.stderr, "ERROR: {} doesn't parse as YAML", \
            format(filename)
        continue

    services = juju_status.get('services', None)
    if not services:
        print >> sys.stderr, "ERROR: no juju services found from {}".format(
            filename)
        continue
    print "\n# juju relation matrix for {}:".format(filename)
    sys.stdout.flush()
    print_relations_matrix(services, cmd_args)

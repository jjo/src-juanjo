#!/usr/bin/env python
# Author: JuanJo Ciarlante <jjo@canonical.com>
import time
#import os
#import string
import re
import socket
import sys


PROC_STAT_FIELDS = ['cpu', 'user', 'nice', 'system', 'idle', 'iowait', 'irq',
                    'softirq', 'steal', 'guest', 'nn10']
PROC_DISKSTAT_FIELDS = ['major', 'minor', 'dev', 'reads', 'readsmerged',
                        'sectorreads', 'readms', 'writes', 'writesmerged',
                        'sectorwrites', 'writems', 'ioscurrent', 'ioms',
                        'iomsweighted']

try:
    PREFIX=sys.argv[1]
except IndexError:
    print >> sys.stderr, ("Usage: {prog} <carbon-prefix>\n"
                          "   eg. {prog} host.$(hostname)".format(
                              prog=sys.argv[0]))
    sys.exit(1)

def carbon_print(nameval):
    print "{}.procinfo.{} {}".format(PREFIX, nameval, int(time.time()))


for line in open('/proc/stat'):
    fields = re.findall(r"[\w]+", line)
    if re.match('^cpu', line):
        linedata = zip(PROC_STAT_FIELDS, fields)
        fieldname = linedata[0]
        fieldvals = linedata[1:]
        for name, val in fieldvals:
            if int(val):
                carbon_print("{}.{}.{} {}".format(
                    fieldname[0], fieldname[1], name, val))
    elif len(fields) == 2:
        carbon_print("stat.{}.{}".format(fields[0], fields[1]))
    elif re.match('^(softirq|intr)', fields[0]):
        for i in xrange(1, len(fields) - 1):
            if int(fields[i]):
                carbon_print("stat.{}.{} {}".format(
                    fields[0], i, fields[i]))

for line in open('/proc/meminfo'):
    fields = re.findall(r"[\w()]+", line)
    carbon_print("mem.{} {}".format(fields[0].lower(), fields[1]))

for line in open('/proc/diskstats'):
    fields = re.findall(r"[\w]+", line)
    linedata = zip(PROC_DISKSTAT_FIELDS, fields)
    fieldname = linedata[2]
    fieldvals = linedata[3:]
    for name, val in fieldvals:
        if int(val):
            carbon_print("disk.{}.{}.{} {}".format(
                fieldname[0], fieldname[1], name, val))

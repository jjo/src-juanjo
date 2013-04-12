#!/usr/bin/env python
# Author: JuanJo Ciarlante <jjo@canonical.com>
# Copyright 2012, Canonical Ltd.
#
"""
Parse several Linux /proc entries into graphite/carbon line output,
for metrics like: cpu, mem, disk, net
"""
import time
import re
import sys
# pylint: disable=C0103,C0111


PROC_STAT_FIELDS = ['cpu', 'user', 'nice', 'system', 'idle', 'iowait', 'irq',
                    'softirq', 'steal', 'guest', 'nn10']
PROC_DISKSTAT_FIELDS = ['major', 'minor', 'dev', 'reads', 'readsmerged',
                        'sectorreads', 'readms', 'writes', 'writesmerged',
                        'sectorwrites', 'writems', 'ioscurrent', 'ioms',
                        'iomsweighted']

PROC_LOADAVG_FIELDS = ['t_1', 't_5', 't_15', 'ps_running', 'ps_total']

try:
    PREFIX = sys.argv[1]
    TIMERES = sys.argv[2]
except IndexError:
    print >> sys.stderr, ("Usage: {prog} <carbon-prefix> <resolution>\n"
                          "   eg. {prog} host.$(hostname) 10min".format(
                              prog=sys.argv[0]))
    sys.exit(1)


def carbon_print(metricname, metricval):
    print "{}.procinfo.{}.{} {} {}".format(PREFIX, metricname, TIMERES,
                                           metricval, int(time.time()))


for line in open('/proc/stat'):
    fields = re.findall(r"[\w]+", line)
    if re.match('^cpu', line):
        linedata = zip(PROC_STAT_FIELDS, fields)
        fieldname = linedata[0]
        fieldvals = linedata[1:]
        for name, val in fieldvals:
            if int(val):
                carbon_print("{}.{}.{}".format(
                    fieldname[0], fieldname[1], name), val)
    elif len(fields) == 2:
        carbon_print("stat.{}".format(fields[0]), fields[1])
    elif re.match('^(softirq|intr)', fields[0]):
        for i in xrange(1, len(fields) - 1):
            if int(fields[i]):
                carbon_print("stat.{}.{}".format(
                    fields[0], i), fields[i])

for line in open('/proc/meminfo'):
    fields = re.findall(r"[\w()]+", line)
    carbon_print("mem.{}".format(fields[0].lower()), fields[1])

for line in open('/proc/diskstats'):
    fields = re.findall(r"[\w]+", line)
    linedata = zip(PROC_DISKSTAT_FIELDS, fields)
    fieldname = linedata[2]
    fieldvals = linedata[3:]
    for name, val in fieldvals:
        if int(val):
            carbon_print("disk.{}.{}.{}".format(
                fieldname[0], fieldname[1], name), val)

for line in open('/proc/loadavg'):
    fields = re.findall(r"[\w.]+", line)
    linedata = zip(PROC_LOADAVG_FIELDS, fields)
    for name, val in linedata:
        carbon_print("loadavg.{}".format(name), val)

for line in open('/proc/net/sockstat'):
    fields = re.findall(r"[\w.]+", line)
    for i in xrange(1, len(fields), 2):
        carbon_print("sockstat.{}.{}".format(
            fields[0].lower(), fields[i]), fields[i + 1])

for idx, line in enumerate(open('/proc/net/snmp')):
    if (idx % 2 == 0):
        fieldnames = re.findall(r"[\w.]+", line)
    else:
        fieldvals = re.findall(r"[\w.]+", line)
        for i in xrange(1, len(fieldnames)):
            carbon_print("snmp.{}.{}".format(
                fieldnames[0].lower(), fieldnames[i].lower()), fieldvals[i])

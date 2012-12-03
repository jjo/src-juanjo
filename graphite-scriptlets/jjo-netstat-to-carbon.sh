#!/bin/bash
# netstat-to-carbon.sh: parse linux's /proc/net snmp entries, transform
#                       to stdout suitable for carbon linereceiver
#
# Author: JuanJo Ciarlante <jjo@canonical.com>
# Copyright 2012, Canonical Ltd.
# License: GPLv3
set -u
PREFIX=${1:-users.jjo.host.$HOSTNAME.netstat.stats}
PERIOD=${2:-10min}

TSTAMP="$(date +%s)"
get_metrics() {
    awk '(NR%2==1){ sub(":","",$1); for(i=2;i<NF;i++) { fieldname[i]=$1 "." $i }} (NR%2==0){ for(i=2;i<NF;i++) { printf("%s %d\n", fieldname[i], $i);}}' /proc/net/snmp /proc/net/netstat
}

# Add carbon-isms to <var> <value> lines
carbonify() {
    sed -r "s/([^ ]+) (.*)/${PREFIX}.\1.${PERIOD} \2 ${TSTAMP}/"
}
get_metrics | carbonify

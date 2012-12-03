#!/bin/bash
# squid-to-carbon.sh: query squid stats via SNMP, transform them
#                     to stdout suitable for carbon linereceiver
#
# Author: JuanJo Ciarlante <jjo@canonical.com>
# Copyright 2012, Canonical Ltd.
# License: GPLv3
set -u
PREFIX=${1:?missing carbon node prefix, e.g.: production.host.${HOSTNAME}.squid.stats}
PERIOD=${2:?missing period, e.g.: 10min}
HOSTPORT=${3:?missing snmp hostport, e.g.: localhost:3401}
SNMPCOM=${4:?missing snmp community, e.g.: public}

SNMPWALK="snmpwalk -v 1 -c ${SNMPCOM} -m SQUID-MIB ${HOSTPORT}"
TSTAMP="$(date +%s)"

## You should not need to edit below
METRICS="SysVMsize SysStorage 
SwapMaxSize SwapHighWM SwapLowWM SysPageFaults SysNumReads 
MemMaxSize MemUsage CpuTime CpuUsage MaxResSize NumObjCount
CurrentUnlinkRequests CurrentUnusedFDescrCnt
CurrentResFileDescrCnt CurrentFileDescrCnt CurrentFileDescrMax
ProtoClientHttpRequests HttpHits HttpErrors HttpInKb HttpOutKb
ServerRequests ServerErrors ServerInKb ServerOutKb
CurrentSwapSize SwapMaxSize SwapHighWM SwapLowWM
HttpAllSvcTime HttpMissSvcTime HttpNmSvcTime HttpHitSvcTime
MedianSvcTable MedianSvcEntry MedianTime IcpQuerySvcTime IcpReplySvcTime
IcpPktsSent IcpPktsRecv IcpKbSent IcpKbRecv
RequestHitRatio RequestByteRatio HttpNhSvcTime Clients DnsSvcTime
PeerPingsSent PeerPingsAcked PeerFetches
PeerRtt PeerIgnored PeerKeepAlSent PeerKeepAlRecv"

## Add SQUID-MIB::cache to METRICS variable
METRICS=$(for i in $METRICS; do echo SQUID-MIB::cache${i};done)

# Filter only numeric metrics, cleanup to be only <var> <value>
get_metrics() {
    for i in ${METRICS};do ${SNMPWALK} $i;done | \
        sed -nr "s/SQUID-MIB:://;s/ = (INTEGER|Counter.*|Gauge.*):/ /p"
}

# Add carbon-isms to <var> <value> lines
carbonify() {
    sed "s/ /.${PERIOD} /;s/^/${PREFIX}./;s/\$/ ${TSTAMP}/"
}

# build a sed expression to replace peer number by its name, sed script looks like:
#   s,(cachePeer.*)[.]1[.],\1.appserver1.,
#   s,(cachePeer.*)[.]2[.],\1.appserver2.,
stringify(){
    local sed_num2str="$(${SNMPWALK} SQUID-MIB::cachePeerName | \
        sed -r 's/.*SQUID-MIB::cachePeerName./s,(cachePeer.*)[.]/;s/ = STRING: (.*)/[.],\\1.\1.,/')"
    sed -r "${sed_num2str}"
}
get_metrics | carbonify | stringify

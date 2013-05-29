#!/bin/bash
# Author: JuanJo Ciarlante <juanjosec@gmail.com>
# License: GPLv3
#
# usage:
#   (iptables -L -vx;ip6tables -L -vx) | jjo-iptables-to-carbon.sh
# e.g. output:
#   firewall.iptables.zone_wan_forward.ACCEPT.tcp.--.any.any.anywhere.pogobox.tcp.dpt:ssh.pkts.10min 5 1339534310
#   firewall.iptables.zone_wan_forward.ACCEPT.tcp.--.any.any.anywhere.pogobox.tcp.dpt:ssh.bytes.10min 300 1339534310
#
awk -vprefix=${1:?missing prefix - eg "host.${HOSTNAME}.firewall.iptables"} -v postfix=${2:?missing postfix -eg "10min"} -vts=$(date +%s) '
    { pkts=-1; }
    /^Chain/ { chain=$2 }
    /policy/ { policy=$4; pkts=$5; bytes=$7; $0=sprintf("._policy_.%s", policy); }
    /^ +[0-9]+/ {
        pkts=$1;bytes=$2; $1=""; $2="";
	gsub("[*]", "any");gsub("[.]","_");gsub(" +", ".");
    }
    { if (pkts<0) next;
        printf ( "%s.%s%s.pkts.%s %d %d\n", prefix, chain, $0, postfix, pkts, ts);
        printf ( "%s.%s%s.bytes.%s %d %d\n", prefix, chain, $0, postfix, bytes, ts)
    }'
# vim: sw=4:ts=4:et:ai

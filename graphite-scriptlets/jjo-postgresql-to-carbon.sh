#!/bin/bash
# postgresql-to-carbon.sh: parse PG stats tables, transform
#                       to stdout suitable for carbon linereceiver
#
# Author: JuanJo Ciarlante <jjo@canonical.com>
# Copyright 2012, Canonical Ltd.
# License: GPLv3
set -u
: ${PREFIX:=production.host.$HOSTNAME.postgresql.stats}
: ${PERIOD:=10min}
: ${DATABASES:=$(psql -At -c 'select * from pg_database where datistemplate=FALSE;'|sed 's/|.*//')}

TSTAMP="$(date +%s)"

pg_stat() {
  local metric_db=${1?} metric_table=${2?} metric_node=${3?}
  local awk_script='
          (NR==1){ for(i=0;i<NF;i++) { fieldname[i]=$i } }
          (NR>1) { for(i=2;i<NF;i++) { if (gsub(":"," ", $i)) value=mktime($i); else value=$i;
                                       printf ("%s.%s.%s %d\n", metric_node, $1, fieldname[i], value); }}'
  psql -A ${metric_db} -c "select ${metric_node},* from ${metric_table};" | gawk -v metric_node="${metric_node}" -vFS='|' "${awk_script}"
}

get_metrics(){
  local db=$1
  pg_stat ${db} pg_stat_user_tables   relname
  pg_stat ${db} pg_statio_user_tables relname
  pg_stat ${db} pg_stat_database      datname | sed -nr "s/[.]${db}/.total/p"
  ## slony replication delay:
  value="$(psql -At -c "SELECT MAX(EXTRACT(EPOCH FROM st_lag_time)) FROM _sl.sl_status WHERE st_origin = _sl.getlocalnodeid('_sl') AND st_received!=0;" ${db} 2>/dev/null)"
  test -n "${value}" && echo "repl_delay.slony.max" ${value}
}
# Add carbon-isms to <var> <value> lines
carbonify() {
    local prefix=${PREFIX}.${1?}
    sed -r "s/([^ ]+) (.*)/${prefix}.\1.${PERIOD} \2 ${TSTAMP}/"
}
for db in ${DATABASES};do
    get_metrics ${db} | carbonify db.${db}
done
ps -opid= -C postgres| xargs -I@ sed -rn 's/^se.//p' /proc/@/sched 2>/dev/null|awk -v OFMT=%d '/exec_start/{ nr_procs++;next} { sub(":","",$1);acc[$1]+=$3 } END { acc["nr_procs"]=nr_procs;for (i in acc) printf("%s %d\n", i, acc[i]);}' | carbonify process.sched

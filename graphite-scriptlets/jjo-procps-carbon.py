#!/usr/bin/env python
# Author: JuanJo Ciarlante <jjo@canonical.com>

# use:
#  ps axfww -o user,pid,ppid,ni,pri,cputime,pmem,rss,size,vsize,stat,blocked,nlwp,lstart,etime,cmd|./parse_ps.py /dev/stdin
# e.g. output:
#   users.jjo.host.caimito.procps.rabbitmq.rss.5min 750248 1340292860
#   users.jjo.host.caimito.procps.rabbitmq.vsz.5min 984048 1340292860
#   users.jjo.host.caimito.procps.rabbitmq.nlwp.5min 43 1340292860
#   users.jjo.host.caimito.procps.rabbitmq.cputime_total.5min 612283.0 1340292860

import sys
import time
import os
import string
import re

### TODO(jjo): all below must be argv[]'d
prefix='users.jjo.host.%s.procps' % os.uname()[1]
postfix='5min'
r_array={
    'rabbitmq': '.*beam.smp.*rabbit.*-kernel.*',
    'bash': '.*bash.*',
}
###
cputime_ps_day_re=re.compile('^[0-9]+-')
files = sys.argv[1:]
r_array_c = {}
for k in r_array.keys():
    r_array_c[k]=re.compile(r_array[k])
for file in files:
    try:
      epoch=int(time.mktime(time.strptime(os.path.basename(file), "%Y-%m-%d:%H:%M:%S.ps")))
    except ValueError:
      epoch=int(time.time())
    f=open(file)
    header=next(f)
    i=0
    fieldpos={}
    for fieldname in header.split():
        fieldpos[fieldname]=i
        i=i+1
    for line in f:
        procname=None
        ### TODO(jjo): should accumulate these
        for procname,ps_re in r_array_c.iteritems():
            if ps_re.match(line):
                values=line.split()
                # trick: use ps output for 'TIME': [days-]hours:min:secs
                #        for strptime against epoch, to get seconds
                cputime_ps=values[fieldpos['TIME']]
                if cputime_ps_day_re.match(cputime_ps):
                    cputime_total=time.mktime(time.strptime("1970-01-%s" % cputime_ps,"%Y-%m-%d-%H:%M:%S"))
                else:
                    cputime_total=time.mktime(time.strptime("1970-01-01-%s" % cputime_ps,"%Y-%m-%d-%H:%M:%S"))
                print '%s.%s.%s.%s' % (prefix, procname, 'rss', postfix), values[fieldpos['RSS']], epoch
                print '%s.%s.%s.%s' % (prefix, procname, 'vsz', postfix), values[fieldpos['VSZ']], epoch
                print '%s.%s.%s.%s' % (prefix, procname, 'nlwp', postfix), values[fieldpos['NLWP']], epoch
                print '%s.%s.%s.%s' % (prefix, procname, 'cputime_total', postfix), cputime_total, epoch

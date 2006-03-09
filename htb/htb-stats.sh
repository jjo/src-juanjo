#!/bin/bash
# Author: JuanJo Ciarlante <jjo-nospam@mendoza.gov.ar>
# License: GPLv2+
#
# $Id: htb-stats.sh,v 1.22 2006/03/09 01:11:36 jjo Exp $
#
# Quick htb stats script: parses "tc -s class show ..." output
# plus: tries to label major:minor classid from 
# htb.init or tcng.init config files.
#
# For your safety: non-root friendly :-) 
# Use as:
#    ./htb-stats.sh           #defaults to eth0
#    ./htb-stats.sh  wlan0
#
DEV=${1:-eth0}
: ${TCNG_CONF:=/etc/sysconfig/tcng-configs/global.tcc}
: ${HTB_INIT_DIR:=/etc/sysconfig/htb}
: ${TC_BIN:=tc}
PRINT_FMT="%-14s %4s %10s %10s %10s %-18s %s\n"

#
#   tcng support:
### 1) Assumes your TCNG config file is /etc/sysconfig/tcng-configs/global.tcc
###    (tcng.init)
### 2) Creates a label map using "tcc -l ...", which *REQUIRES* 
###    your entries tagged with:    tag "label for this traffic" , eg:
###     : 
###     class ( rate 64kbps, ceil 128kbps, tag "wan_total") { 
###       $wan_ssh   = class (rate 32kbps, ceil 128kbps, prio 0, tag "wan_ssh") { sfq; };
###       $wan_http  = class (rate 16kbps, ceil 64kbps,  prio 1, tag "wan_http") { sfq; };
###       $wan_other = class (rate 16kbps, ceil 64kbps,  prio 2, tag "wan_other"){ sfq; }; 
###     };
###
#
#   htb.init support:
### 1) Uses /etc/sysconfig/htb filenames: DEV-n1:n2:...:minor.label 
###    for getting major:minor label  (with major=1 hardcoded in htb.init)
###    with no special "naming" requirements
###

PATH=$PATH:/usr/sbin:/sbin
if [ $UID -eq 0 ];then
	TCNG_MAP=/var/run/tcng.map
else
	TCNG_MAP=${TMPDIR:-/tmp}/$LOGNAME-tcng.map
fi
# tcng_load_DICT: 
#   Create assoc array: DICT_label_class_${DEV}_${classid}_X
#   from "tcc -l ..." map' labels
tcng_load_DICT() {
	local what classid tag resto classid
	test -f ${TCNG_CONF} || return 1
	test $TCNG_MAP -ot ${TCNG_CONF} && \
	tcc -l $TCNG_MAP ${TCNG_CONF} > /dev/null
	#eg:
	#class eth1:2:4 labelblah /etc/sysconfig/tcng-configs/global.tcc 75
	#qdisc eth1:5 - /etc/sysconfig/tcng-configs/global.tcc 75
	while read what classid tag resto;do
	case "$what" in
		qdisc|class) 
			test "TAG$tag" = "TAG-" && continue
			# trasformar classid:
			# eth0:2:20  (decimal) -> eth0_2_14  (hexa) 
			classid=$(printf "%s_%x_%x" ${classid//[:]/ })
			eval "DICT_label_${what}_${classid}_X=\"$tag\""
			;;
	esac
	done < $TCNG_MAP
}
# htb_load_DICT: 
#   Create assoc array: DICT_label_class_${DEV}_${classid}_X
#                  and: DICT_filename_class_${DEV}_${classid}_X
#   from /etc/sysconfig/htb/ filenames
htb_load_DICT() {
	MAJOR=1  ## hardcoded in htb.init AFAIK
	test -d ${HTB_INIT_DIR} || return 1
	local aux filename minor label
	while read filename;do
		### get minor,label from filename as: DEV-n1:n2:...:minor.label 
		aux=${filename##$DEV-}
		aux=${aux##*:}
		minor=${aux%%.*}
		label=${aux#*.}
		eval "DICT_label_class_${DEV}_${MAJOR}_${minor}_X=\"$label\""
		eval "DICT_filename_class_${DEV}_${MAJOR}_${minor}_X=\"$filename\""
	done < \
	<(cd ${HTB_INIT_DIR} && ls $DEV*[:-]* 2>/dev/null)
}
#
# to_kbits: Convert passed rate to kbits
#
# ugly global variable instead of eg. ret=$(func arg)
# to avoid fork()ing (+speed)
# 
to_kbits() {
	RET_to_kbits=	#global
	case "$1" in
	*bps) RET_to_kbits="$((${1%bps}*8/1000))kbps";;
	*Kbit) RET_to_kbits="$((${1%Kbit}*1024/1000))kbps";;	# units mess (?)
	*[0-9]bit) RET_to_kbits="$((${1%bit}/1000))kbps";;
	__*Kbit) RET_to_kbits="$1";;	# else: eg. "Kbit" is returned as-is
	*) RET_to_kbits="$1";;	# as-is
	esac
}
#
# do_stat: Core function
#   Parses "tc -s class show ..." output, creating synthetic output:
#	"$classid" "$backlog" "$rate" "$confrate" "$confceil" "$label" "$filename" 
#   where {label, filename} are queried from DICT_xxxx assoc arrays
#
do_stat() {
  local classid rate backlog confceil confrate confparent
  local classid_underscore label filename
  while read line ;do
	#echo $line
	set -- $line
	case "$1-$2-$3-$4" in
	class-htb-*-*) 		classid=$3;rate=0;backlog=" ";confceil=0;confrate=0;confparent=0:0;
				while test -n "$1";do
					case "$1" in
					rate) confrate=$2;shift;;
					ceil) confceil=$2;shift;;
					parent) confparent=$2;shift;;
					esac
					shift
				done
				to_kbits "$confceil";confceil="$RET_to_kbits"
				to_kbits "$confrate";confrate="$RET_to_kbits"
				continue;;
	rate-*-*) 
			test "$4" = "backlog" && backlog="$5"
			rate=$2
			continue
			;;
	tokens:*) ;;
	*) continue;;
	esac
	classid_underscore="${classid//[:]/_}"  ## convert ':' to '_'
	vname="DICT_label_class_${DEV}_${classid_underscore}_X"
	label=${!vname}		## get label from DICT_label_{...}
	vname="DICT_filename_class_${DEV}_${classid_underscore}_X"
	filename=${!vname}	## get filename from DICT_filename_{...}
	to_kbits "$rate";rate=$RET_to_kbits
	classid=$(printf "%02x:%02x->%02x:%02x" 0x${confparent//[:]/ 0x} 0x${classid//[:]/ 0x})
	printf "$PRINT_FMT" "$classid" "$backlog" "$rate" "$confrate" "$confceil" "$label" "$filename" 
  done < \
  <(${TC_BIN} -s class show dev $DEV)
}

tcng_load_DICT || htb_load_DICT || {
	echo "ERROR: No $TCNG_CONF (tcng) neither $HTB_INIT_DIR (htb) found."
	exit 1
}
printf "$PRINT_FMT" "CLASSID" "q." "rate" "RATE" "MAX" "LABEL" ""
do_stat | sort | sed -e 's/^0/ /'  -e 's/>0/> /' 

#
# $Log: htb-stats.sh,v $
# Revision 1.22  2006/03/09 01:11:36  jjo
# . do error if not tcng or htb config. found
#
# Revision 1.21  2006/03/08 15:53:33  jjo
# . docs, some func renames
#
# Revision 1.20  2006/03/08 15:09:41  jjo
# . spelling
#
# Revision 1.19  2006/03/08 15:06:08  jjo
# . optimization: use "eval varname=value" and "${!varname}" for creating and using DICTs (assoc arrays), instead of "eval funcname(){ echo $value }" construct.
#
# Revision 1.18  2006/03/08 02:19:53  jjo
# . new htb_init_load function to generalize classid->{label,file} mapping
#
# Revision 1.17  2006/03/08 01:14:16  jjo
# . allow tc exec override with TC_BIN env. var
#
# Revision 1.16  2006/03/08 01:06:35  jjo
# . recalc "bit" (bps) to kbps
#
# Revision 1.15  2006/03/07 15:56:22  jjo
# . (mini) document tcng support
#
# Revision 1.14  2005/09/13 14:15:36  jjo
# . minor tweaks
#
# Revision 1.13  2005/09/08 23:15:33  jjo
# . format adjustments
#
# Revision 1.12  2005/09/08 04:12:52  jjo
# also show (and sort) parent
#
# Revision 1.11  2005/09/05 14:31:10  jjo
# . added (configured) rate to output
#
# Revision 1.9  2005/09/02 04:30:11  jjo
# mess with units (kbits vs kbps, etc)
#
# Revision 1.8  2005/09/01 15:59:14  jjo
# agregado "ceil" (MAX) y encabezados
#
# Revision 1.7  2005/09/01 04:25:32  jjo
# usar "shopt -s extglob" para + precision; TCNG_MAP adaptable a root/no-root
#
# Revision 1.6  2005/09/01 03:21:57  jjo
# . yeaH!: mapped (decimal) tcng.map number to (hexa) tc -s class show
#
# Revision 1.3  2003/09/12 16:35:46  jjo
# . boring doc
#
# Revision 1.2  2003/09/12 16:23:07  jjo
# . 1st public release
# 
#

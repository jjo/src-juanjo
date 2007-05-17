#!/bin/bash
### ipv6-setup6to4.sh: print commands to setup ipv6 6to4 tunnel under Linux.
###
### Author: JuanJo Ciarlante - jjo O mendoza gov ar
### usage: 
###    ipv6-setup6to4.sh                      #just SHOW
###    ipv6-setup6to4.sh       | sudo sh -x   #do it by pipeing to "sh"     
###    ipv6-setup6to4.sh auto  | sudo sh -x   #same as above
###    ipv6-setup6to4.sh auto eth0=1::1/64    #also SHOW howto setup eth0 with $IP6TO4_PREF:1::1/64
###    ipv6-setup6to4.sh auto eth0=1::1/64 wlan0=2::1/64
###    ipv6-setup6to4.sh -r ...               #reverse the commands (eg: add -> del, etc)
export PATH="/sbin:/usr/sbin:$PATH"
test "$1" = "-r" && { shift;$0 "$@" | tac | sed -re 's/\badd\b/del/' -e 's/\bup\b/down/'; exit $?; }
IP4_ADDR="${1:-auto}"
shift
IFACE_IP6NODE="$2" # eg:  "eth0=1::1"
if [ "$IP4_ADDR" = "auto" ];then
	### If not passed, guess out IPv4 global src
	IP4_ADDR="$(ip route get 1.0.0.0)"
	test -z "$IP4_ADDR" && exit 0
	IP4_ADDR="${IP4_ADDR##*src }"
	IP4_ADDR="${IP4_ADDR%% *}"
fi

### Compute the 6TO4 tunnel IPv6 address:
### use awk instead of builtin printf for busybox compat (openwrt friendly ;-)
IP6TO4_PREF=$(echo $IP4_ADDR | awk -v "FS=[.]" ' { printf ("2002:%x%02x:%x%02x",$1,$2,$3,$4) }')

ip() {
	echo ip "$@"
}
### Print to stdout the commands to setup the tunnel:
echo "IP4_ADDR=$IP4_ADDR"
echo "IP6TO4_PREF=$IP6TO4_PREF"
echo "#check you allow ipv6 encap: iptables -I INPUT -p 41 -d $IP4_ADDR" 
ip tunnel add tun6to4 mode sit remote any local $IP4_ADDR ttl 64
ip addr flush dev tun6to4 2\>/dev/null
ip link set dev tun6to4 up
ip addr add $IP6TO4_PREF::1/16 dev tun6to4
ip route add ::/96 dev tun6to4 
ip route add 2000::/3 via ::192.88.99.1 dev tun6to4 metric 1
test -z "$*" && echo "#you may do something like:  ip -6 addr add $IP6TO4_PREF:0001::1/64 dev eth0"
for iface_ip6node in "$@";do
	iface=${iface_ip6node%%=*}; ip6node=${iface_ip6node#*=}
	ip addr add $IP6TO4_PREF:$ip6node dev $iface
done
echo
test -t 1 && echo "#NOTHING done, use me as: $0   |sudo sh -x"

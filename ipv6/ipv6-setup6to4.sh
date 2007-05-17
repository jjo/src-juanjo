#!/bin/bash
### usage: 
###    ipv6-setup6to4.sh
###    ipv6-setup6to4.sh auto            #same as above
###    ipv6-setup6to4.sh auto eth0=1::1  #also setup eth0 with $IP6TO4_PREF:1::1
###    ipv6-setup6to4.sh auto eth0=1::1  wlan0=2::1
export PATH="/sbin:/usr/sbin:$PATH"
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
### Setup the tunnel
echo "IP4_ADDR=$IP4_ADDR"
echo "IP6TO4_PREF=$IP6TO4_PREF"
echo "#check you allow ipv6 encap: iptables -I INPUT -p 41 -d $IP4_ADDR" 
ip tunnel del tun6to4
ip tunnel add tun6to4 mode sit remote any local $IP4_ADDR ttl 64
ip link set dev tun6to4 up
ip addr add $IP6TO4_PREF::1/16 dev tun6to4
ip route add ::/96 dev tun6to4 
ip route add 2000::/3 via ::192.88.99.1 dev tun6to4 metric 1
test -n "$*" && echo "#you may do something like:  ip -6 addr add $IP6TO4_PREF:0001::1/64 dev eth0"
for iface_ip6node in "$@";do
	iface=${iface_ip6node%%=*}; ip6node=${iface_ip6node#*=}
	ip addr add $IP6TO4_PREF:$ip6node dev $iface
	ip route add $IP6TO4_PREF:${ip6node%%:*}::/64 dev $iface
done
echo
test -t 1 && echo "#NOTHING done, use me as: $0   |sudo sh -x"

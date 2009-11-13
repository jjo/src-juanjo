#!/bin/sh
###   nctun.sh: Tunel "tuntap" sobre usando shell y nc (netcat), algo así
###             como una VPN sin la 'P' ;-) (se podría usar cryptcat para la 'P').
###  ./nctun.sh  (para  ver el uso)
###     Author: JuanJo  jjo (.) mendoza.gov.ar
###    License: GPLv2+
###   Requiere: modulo "tuntap", nc (netcat) y utilidad de ayuda: ./tuntap-eame-el-descriptor
usage() { echo "
Uso: $0 IPint_local IPint_remota udp_port [IPext_remota]
Ej. server# $0 1.1.1.1  2.2.2.2  9999
    client# $0 2.2.2.2  1.1.1.1  9999 <server_ip>
    client\$ ping 1.1.1.1";
}
runcmd() { echo + "$@" >&2; "$@";}

IPint_local=${1} IPint_remota=${2} UDP_PORT=${3?"$(usage)"}
IPext_remota=${4}
which nc >/dev/null                 || { echo "Falta nc (netcat). Instalalo"; }
test -x ./tuntap-eame-el-descriptor || { echo "Falta ./tuntap-eame-el-descriptor. Compilalo."; }
test -w /dev/net/tun                || { echo "No puedo abrir /dev/net/tun. Cargar modulo tuntap y ejecutame como root.";}

### 4-pasos-4:
###(1)###  Abre /dev/net/tun en el fd=3:
exec 3<> /dev/net/tun || exit 1

###(2)### ... y lo convierte en un "tun" device con ./tuntap-eame-el-descriptor
dev=$(runcmd ./tuntap-eame-el-descriptor 3 "jjo%d") || exit 2  
echo "DEV=$dev"

###(3)### Configura el dispositivo para IP
runcmd ifconfig $dev $IPint_local pointopoint $IPint_remota || exit 3

###(4)### Lanza netcat eternamente _escribiendo_/_leyendo_ del fd=3 desde/hacia el peer 

# ufffa: netcat requiere -p para listen? (dep. de la version :-P )
nc -h 2>&1 | egrep -q "inbound.*-p" && _P="-p" 
while :;do
	## Si no hay IPext_remota: -l (listen, lado server)
	runcmd nc -u ${IPext_remota:- -l $_P} ${UDP_PORT}  <&3 >&3   #-u: UDP
	sleep 2
done

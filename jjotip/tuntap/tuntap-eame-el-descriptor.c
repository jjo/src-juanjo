/* tuntap-eame-el-descriptor: creates tun device from opened "fd" (on /dev/net/tun) 
 *                            and "devname%d" template devname
 *  Author: JuanJo  jjo (.) mendoza.gov.ar
 * License: GPLv2+
 *
 * Compile with:  make tuntap-eame-el-descriptor    */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ioctl.h>
#include <net/if.h>
#include <linux/if_tun.h>
int main(int argc, char *argv[]) {
	struct ifreq ifr;
	int fd;
	if (argc!=3) {
		fprintf(stderr, "Uso: %s fdnum \"devname%%d\"\n"
				" ej: bash# exec 3<>/dev/net/tun && %s 3 tunel%%d\n", argv[0], argv[0]);
		return 255;
	}
	fd=atoi(argv[1]);

	memset(&ifr, 0, sizeof(ifr));
	ifr.ifr_flags = IFF_TUN | IFF_NO_PI;
	strncpy(ifr.ifr_name, argv[2], IFNAMSIZ);
	if (ioctl(fd, TUNSETIFF, (void *) &ifr)<0) {
		perror("ioctl(TUNSETIFF)");
		return 1;
	}
	puts(ifr.ifr_name);
	return 0;
}

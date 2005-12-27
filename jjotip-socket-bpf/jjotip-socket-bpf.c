/*
 *  jjotip-socket-bpf.c: Create blind UDP socket using BPF over SOCK_DGRAM (2005/12/27)
 *
 *  Author: JuanJo ... jjo () mendoza gov ar
 *  License: GPLv2+
 */
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <linux/types.h>  
#include <linux/filter.h>

static int create_socket_bind_and_ignoreit(u_int16_t bind_port) {
	int sock=-1;
	struct sockaddr_in bindaddr = {
		.sin_family = AF_INET,
		.sin_addr.s_addr   = htonl(INADDR_ANY), /* network byte-order */
		.sin_port   = bind_port    /* network byte-order */
	};

	/* This is BPF at PF_INET/SOCK_DGRAM level (8 bytes UDP header + DATA) */
	struct sock_filter bpf_code[]= { 
		{ 0x6, 0, 0, 0x00000000 }, /* ret #0 : accept 0 bytes -> IGNORE IT */
	};                            
	struct sock_fprog filter = {
		.len = sizeof(bpf_code)/sizeof(*bpf_code), /* how many instructions */
		.filter = bpf_code,
	};

	if ((sock=socket(PF_INET, SOCK_DGRAM, 0))<0) {
		perror("socket");
		goto fail;
	}

	if (bind(sock, (struct sockaddr *) &bindaddr, sizeof (bindaddr)) < 0) {
		perror("bind");
		goto fail;
	}

	/* attach "ignoring" filter  */
	if(setsockopt(sock, SOL_SOCKET, SO_ATTACH_FILTER, &filter, sizeof(filter))<0){
		perror("setsockopt");
		goto fail;
	}
	return sock;

fail:
	if (sock>=0) close(sock);
	return -1;

}
int main(void) {
	int sock;
	int n;
	int port;
	char buf[2048];

	port=htons(6969);

	sock = create_socket_bind_and_ignoreit(port);
	if (sock<0) return 2;
	while (1) {
		memset(buf, 0, sizeof(buf));
		n = recvfrom(sock,buf,sizeof(buf),0,NULL,NULL);
		if (n<=0) break;
		printf("n=%d str=%s\n",n, buf);
	}

}
/* See:
	tcpdump -d <filtro> ; tcpdump -dd <filtro>
	/usr/include/pcap-bpf.h
	http://www.gsp.com/cgi-bin/man.cgi?section=4&topic=bpf
 */

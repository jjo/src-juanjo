/*
 *  jjotip-socket-bpf-match_data.c: Use BPF to match a 4 bytes string (and ignore the rest)
 *
 *  Author: JuanJo ... jjo () mendoza gov ar
 *  License: GPLv2+
 */
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netinet/udp.h>
#include <arpa/inet.h>
#include <linux/types.h>  
#include <linux/filter.h>

/*
Mini exercise:

tcpdump -dd "ether[0:4]=0x01020304" -s 2048
{ 0x20, 0, 0, 0x00000000 },
{ 0x15, 0, 1, 0x01020304 },
{ 0x6, 0, 0, 0x00000800 },
{ 0x6, 0, 0, 0x00000000 },
tcpdump -d "ether[0:4]=0x01020304" -s 2048
(000) ld       [0]
(001) jeq      #0x01020304      jt 2    jf 3
(002) ret      #2048
(003) ret      #0
*/

static int create_socket_bind_and_pass4(u_int16_t bind_port, const char *str4bytes) {
	int sock=-1;
	struct sockaddr_in bindaddr = {
		.sin_family = AF_INET,
		.sin_addr.s_addr   = htonl(INADDR_ANY), /* network byte-order */
		.sin_port   = bind_port    /* network byte-order */
	};
	int match4 = (int)*(int*)(str4bytes);
	/* This is BPF at PF_INET/SOCK_DGRAM level (8 bytes UDP header + DATA) */
	struct sock_filter bpf_code[]= { 
	/* load 32bits from offset*/
		{ 0x20, 0, 0, 0x00000000 + sizeof(struct udphdr) },
	/* jump-eq true:+0 false:+1 */
		{ 0x15, 0, 1, ntohl(match4) }, /* argument must be host byte order */
	/* return 1500 (OK) */
		{ 0x6, 0, 0, 1500 },
	/* return 0 (nop) */
		{ 0x6, 0, 0, 0 },
	};                            
	struct sock_fprog filter = {
		.len = sizeof(bpf_code)/sizeof(*bpf_code), /* how many instructions */
		.filter = bpf_code,
	};

	printf("m=%08x\n", ntohl(match4));
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
static void usage(const char *wtf);
int main(int argc, const char *argv[]) {
	int sock;
	int n;
	char buf[2048];
	int port; const char *str;

	if (argc != 3) { usage("Bad number of arguments"); };
	port=atoi(argv[1]);
	if (port<=0 || port> 65535) usage("Bad port number");
	str=argv[2];
	if (strlen(str)!=4) usage("String must be 4 chars");
	sock = create_socket_bind_and_pass4(htons(port), str);
	if (sock<0) return 2;
	printf("So far, so good ... test me with:\n"
		"  $ nc -u localhost %d\n"
		"  %s...blablah...\n"
		"  <noisssssse>...\n", port, str);
	while (1) {
		memset(buf, 0, sizeof(buf));
		n = recvfrom(sock,buf,sizeof(buf),0,NULL,NULL);
		if (n<=0) break;
		printf("READ n=%d str=%s\n",n, buf);
	}
	return 0;
}

static void usage(const char *wtf) {
	fprintf(stderr, "ERROR: %s.\nusage: progname <port> <4-byte-string>\n   eg: progname 6969 \"hola\"\n", wtf);
	exit(255);
}
/* See:
	tcpdump -d <filtro> ; tcpdump -dd <filtro>
	/usr/include/pcap-bpf.h
	http://www.gsp.com/cgi-bin/man.cgi?section=4&topic=bpf
 */

/*
 *  zocket.c: connect a socket, block its data stream, write data @children:
 *            show zombie and socket lifetime afterwards
 *
 *  Author: JuanJo: jjo () google com
 *  License: GPLv2+
 */
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/wait.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <assert.h>
#if __linux__
#include <linux/filter.h>
#endif

/* quickie wrapper over syscall error checking */
#define ERR_IF(cond) do { if(cond) { perror( #cond ); abort(); } } while (0)

static int block_fromto(int sockfd, const struct sockaddr_in *sp, 
		const struct sockaddr_in *dp) {
#ifdef __linux__
	/* 
	 * Push a BPF into _this_ socket only, interesting enough
	 * this seems to be a linux-only feature, BSD has this available
	 * only at accept().
	 */
	struct sock_filter bpf_blockme[]= { 
		BPF_STMT(BPF_RET+BPF_K, 0), /* just accept 0 bytes ;) */
	};                            
	struct sock_fprog filter = {
		sizeof(bpf_blockme)/sizeof(*bpf_blockme), bpf_blockme,
	};

	ERR_IF(setsockopt(sockfd, SOL_SOCKET, SO_ATTACH_FILTER, 
				&filter, sizeof(filter))<0);
#else /* assuming BSD: block at PF level */
	char cmd[1024];
	cmd[sizeof cmd-1]=0;
	snprintf(cmd, sizeof cmd-1,
		"echo block drop out inet proto tcp "
		"from %s port %d to %s port %d| pfctl -f-",
			/* leaking but effective ... */
			strdup(inet_ntoa(sp->sin_addr)), htons(sp->sin_port),
			strdup(inet_ntoa(dp->sin_addr)), htons(dp->sin_port));
	printf("====== configuring pf:\n+ %s\n", cmd);
	ERR_IF(system(cmd)<0);
#endif
	return 0;
}
int main(int argc, const char *argv[]) {
	int sock;
	int pid;
	int syncpipe[2];
	unsigned n;
	char cmd[2048];
	struct sockaddr_in dest,me;

#ifndef __linux__
	/* need to use /sbin/pfctl for blocking pkt stream if !linux */
	assert(getuid()==0);
#endif
	if (argc != 3) { 
		fprintf(stderr, "ERROR: Usage: %s <ip> <port>\n", argv[0]);
		exit(255);
	}
	dest.sin_family = AF_INET;
	ERR_IF( inet_aton(argv[1], &dest.sin_addr) == 0);
	dest.sin_port=htons(atoi(argv[2]));

	sock = socket(AF_INET, SOCK_STREAM, 0);
	ERR_IF(sock <0);
	ERR_IF(connect (sock, (struct sockaddr *)&dest, sizeof dest) < 0);
	n=sizeof me;
	getsockname(sock, (struct sockaddr *)&me, &n);

	/* unbuffer stdout */
	setbuf(stdout, NULL);
	/* block (output) data stream */
	block_fromto(sock, &me, &dest);
	pipe(syncpipe);
	for(n=3;n;n--) {
		switch(pid=fork()) {
			case 0:
				close(syncpipe[0]);
				write(sock, "1234567890", 10);
				_exit(0);
			case -1: ERR_IF(1);
		}
	}
	close(sock);
	/* sync to children death */
	read(syncpipe[0], NULL, 0);
	cmd[sizeof cmd -1]=0;
	snprintf(cmd, sizeof cmd -1, 
			"ps -o pid,ppid,stat,command|egrep [z]ocket;"
			"netstat -tn|egrep '[.:]%d .*[.:]%d'",
			ntohs(me.sin_port), ntohs(dest.sin_port));
	/* this will show the zombies and the socket send-q (as netstat -tn) */
	printf("====== BEFORE wait() ======\n+ %s\n", cmd); system(cmd);
	while(wait(NULL)>0);
	/* obviously the zombies are gone, what about the (orphaned) socket ?*/
	printf("====== AFTER  wait() ======\n+ %s\n", cmd); system(cmd);
	return 0;
}

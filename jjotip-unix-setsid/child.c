#include <stdio.h>
#include <unistd.h>
#include <sys/signal.h>
#include <fcntl.h>

char *ptsname(int);
extern int errno;
char *quiensoyio="padre";
#define error(format, args...)  \
      fprintf (stderr, format , ## args)

#define debug(format, args...)  \
      fprintf (stderr, format , ## args)
pty_allocate(int *ptyfd, int *ttyfd, char *namebuf, int namebuflen) {
	int ptm;
	char *pts;

	ptm = open("/dev/ptmx", O_RDWR | O_NOCTTY);
	if (ptm < 0) {
		error("/dev/ptmx: %.100s", strerror(errno));
		return 0;
	}
	if (grantpt(ptm) < 0) {
		error("grantpt: %.100s", strerror(errno));
		return 0;
	}
	if (unlockpt(ptm) < 0) {
		error("unlockpt: %.100s", strerror(errno));
		return 0;
	}
	pts = ptsname(ptm);
	if (pts == NULL)
		error("Slave pty side name could not be obtained.");
	strncpy(namebuf, pts, namebuflen);
	*ptyfd = ptm;

	/* Open the slave side. */
	*ttyfd = open(namebuf, O_RDWR /* | O_NOCTTY */);
	if (*ttyfd < 0) {
		error("%.100s: %.100s", namebuf, strerror(errno));
		close(*ptyfd);
		return 0;
	}

}
void print_sess() {
	debug("*** %-20s: pid=%d sid=%d ***\n", quiensoyio, getpid(), getpgid(0));
}
void do_ps(const char *str) {
	if (str) debug("\n%s:\n", str);
	system("ps -jf 1>&2");
}

/*
 * Esto ejecuta el hijo luego del fork().
 */
void hand(int sig) {
	printf("***>> %-10s: Ouch! sig=%d <<***\n", quiensoyio, sig);
}
int do_child(int hagolamia) {
	/* Creo mi sesion (si asi me lo pidieron), con lo cual
	 * _NO_ voy a recibir la signal de muerte de papi
	 */
	if (hagolamia) setsid();
	signal(SIGHUP, hand);
	print_sess("hijo");
	sleep(2);	/* zzZZ esperando muerte de papi */
	return 0;
}
/* fin hijo */
int main(int ac, const char *av[]) {
	int ptyfd, ttyfd;
	char buf[256];
	int hp=0;
	/* si paso 'n' como 1er argumento, pongo hp=1 */
	if (ac>1 && av[1][0]=='h') {
		hp=1;
	}
	printf("hp=%d\n", hp);
	/* 
	 * Necesario: bash me lanzo como leader de process group (pgrp), _pero_
	 * attachado a la terminal.
	 * Para que setsid tenga exito (y me desvincule de la tty) 
	 * tengo que asegurarme con un fork(), ver setsid(2)
	 */
	if (fork() != 0) return 0;
	do_ps("PREVIO setsid()");
	setsid();

	do_ps("POST   setsid()");
	/*
	 * Para poder provocar el efecto de:
	 *   muerte de pgrp leader de la tty => SIGHUP al pgrp
	 * tengo que tener _mi_propia_ tty.
	 *
	 * Creo una nueva pty.
	 */
	pty_allocate(&ptyfd, &ttyfd, buf, 256);
	debug("*** pty=%s ***\n", buf);
	switch(fork() ) {
		case -1:	perror("fork()");break;
		case 0:		quiensoyio="hijo";return do_child(hp);break;
		default:	print_sess("padre"); 
	}
	do_ps("POST   pty() y fork()");
	return 0;
}

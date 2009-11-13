/* 
 * SIGPIPE /EPIPE tuto
 * Autor: JuanJo Ciarlante
 *
 * compilar con:
 * 	make jjpipe
 * uso:
 * 	- normal:
 * 		./jjpipe cat
 * 		./jjpipe "tr [a-z] [A-Z]"
 *	- pipe quebrado (con sigpipe la mayor parte de las veces :)
 *		./jjpipe true         (true es un comando que NO CONSUME stdin)
 *	- pipe quebrado ignorando se~al (muestra error 32 --EPIPE--)
 *		./jjpipe -s true
 * 
 * This program is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the
 * Free Software Foundation; either version 2 of the License, or (at your
 * option) any later version.  See <http://www.fsf.org/copyleft/gpl.txt>.
 *
 * This program is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
 * or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
 * for more details.
 */
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <errno.h>
#include <string.h>
#include <sys/signal.h>

#define STR "*** probate este tubo ... ***\n"

extern char *optarg;
extern int optind, opterr, optopt;
int ignore_sigpipe=0;

void show_error(err) {
	printf("-errno=%d %s \"%s\"\n", err, 
			err==32? "EPIPE" : "",
			strerror(err));
}
void sigpipe_handler(int signum) {
	fprintf(stderr, "!uaaaCKKKKK!! SIGPIPE=%d\n", signum);
	exit(1);
}
void parse_opts(int argc, const char *argv[]) {
	while (1) {
		int c;
		c = getopt(argc, (char**)argv, "s");
		if (c == -1)
			break;

		switch (c) {
			case 's':
				ignore_sigpipe++;
				break;
		}
	}
}

int main(int argc, const char *argv[]){
	FILE *fp;
	const char *command;
	if (argc < 2) {
		fprintf(stderr, "uso: jjpipe [-s] comando\n");
		return 1;
	}
	parse_opts(argc, argv);
	command=argv[optind];
	if (ignore_sigpipe) {
		printf("-SIGPIPE: ignorarla\n");
		signal(SIGPIPE, SIG_IGN);
	} else {
		printf("-SIGPIPE: normal\n");
		signal(SIGPIPE, sigpipe_handler);
	}
	printf("-Abriendo pipe a \"%s\" ...\n", command);
	fp=popen(command, "w");
	if (!fp || ferror(fp) || errno>0) goto out;

	printf("-Escribiendo en pipe ...\n");
	fputs(STR,fp);
	if (ferror(fp) || errno>0) goto out;

	printf("-Cerrando pipe ...\n");
	fclose(fp);

out:
	show_error(errno);
	printf("FIN.\n");
	return 0;
}

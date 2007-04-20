/* 
 * fork-espero-el-fin-de-mi-hermano-menor.c
 *
 * Terminacion consecutiva de procesos hijo en orden reverso a su creacio'n
 * respuesta a: http://www.lugmen.org.ar/pipermail/lug-devel/2007-April/000876.html
 *
 * Autor: JuanJo Ciarlante ; jjo en um punto edu punto ar
 * Licencia: GPLv2
 */

#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>

#include <assert.h>

/* Estrategia: la terminacion el siguiente proceso cierra el pipe donde estoy
               durmiendo, y luego termino (y asi' sucesivamente):

	proceso[i-1]	proceso[i] 	proceso[i+1]
					:
			:		read() <=pipe< ...
	:		read() <=pipe<	_exit()
	read() <=pipe<	_exit()
	_exit() 

   Notar que el enfoque NO requiere de arrays, ni tampoco kill()
 */
			                     
int main(int argc, char *argv[]) {
	int i,n;
	int pipefd[2];
	int fdaux=-1;
	char ch;

	assert(argc==2);
	assert( (n=atoi(argv[1])) > 0);

	for (i=0;i<n;i++) {
		assert(pipe(pipefd)==0);
		switch(fork()) {
			case -1: assert(0);break;
			case 0:
				/* hijo: recibe los sig. descriptores ABIERTOS:
				   pipefd[0] y [1]: pipe actual
				   fdaux: lado escritura del pipe previo
				 */

				/* cerrar el lado escritura del pipe actual */
				close(pipefd[1]);

				/* duermo en read() del pipe actual: me despertare'
				   cuando termine el sig. hijo, al cerrarse el lado
				   escritura del presente pipe */
				read(pipefd[0], &ch, 1);

				printf("[%d]: chauuu\n", i);
				/* al salir, naturalmente se cerrarán todos los descriptores;
				   en particular: al cerrarse el lado escritura del pipe previo
					 despertara' el hijo anterior del read() y terminara' */
				_exit(0);

		}
		close(pipefd[0]);

		/* las sig. dos lineas hacen que el PADRE cierre pipefd[1] en el PROX. loop */
		close(fdaux);
		fdaux=pipefd[1];
	}

	/* "disparador": cierra el u'ltimo descriptor de escritura */
	close(fdaux);
	while(wait(NULL)>=0);
	return 0;
}

/* mproc-mutex.c: "global" longlived multi-process pthread_mutex example */

/* 
 * Author: JuanJo Ciarlante,  jjo \o/ um edu ar
 * License: GPLv2
 * Date: Wed Dec 20 09:26:29 ART 2006

 # Explanation:
   pthread_mutex is a mutual exclusion lock usually used un multi-threaded 
   applications.
   This program shows a mutex usage that SURVIVES de timelife of a process
   (hence can be used between processes) by making a shared-memory storage 
   for the pthread_mutex_t object.
   Tested on glibc-2.3+, linux-2.6 .

 # Compilation, just do: egrep make mproc-mutex.c | sh -x  ;-)
   	make mproc-mutex LDLIBS="-lpthread -lrt" CFLAGS=-Wall

 # Usage:

 	./mproc-mutex foo i   #initialize "foo" mutex, will be /dev/shm/foo
 	./mproc-mutex foo l   #lock; call it twice to see it "working"
 	./mproc-mutex foo l   #lock again: will wait until unlock or signalled
 	./mproc-mutex foo u   #unlock 
	rm /dev/shm/foo    #remove it
 */ 

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/types.h>
#include <fcntl.h>
#include <pthread.h>
#include <sys/mman.h>

#define ERR_EXIT(call) do { if ((int)(call)==-1) { perror(#call); exit (EXIT_FAILURE); }} while(0)
#define ERR_EXIT0(call) do { if ((int)(call)!=0) { perror(#call); exit (EXIT_FAILURE); }} while(0)
int main(int argc, char **argv)
{
	int fd;
	pthread_mutex_t *p;
	if (argc!=3)
		{fprintf(stderr, "usage: %s /mutex_file_name {i|l|u}\n", argv[0]);exit(EXIT_FAILURE);}

	ERR_EXIT( fd=shm_open(argv[1], O_RDWR|O_CREAT, 0666) );

	if (*argv[2]=='i') 
		/* expand the shm file to required size */
		ERR_EXIT( ftruncate(fd, sizeof(pthread_mutex_t)) ); 

	/* map the shmfile to process memory */
	ERR_EXIT ( p=mmap(NULL, sizeof(pthread_mutex_t), PROT_READ|PROT_WRITE, MAP_SHARED, fd, 0) );

	/* (i)nitialize  or (l)ock or (u)nlock the mutex */
	switch (*argv[2]) {
		case 'i' : ERR_EXIT0( pthread_mutex_init(p, NULL) );break;
		case 'l' : ERR_EXIT0( pthread_mutex_lock(p)       );break;
		case 'u' : ERR_EXIT0( pthread_mutex_unlock(p)     );break;
	}
	return 0;
}

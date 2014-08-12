GCFLAGS=-I.

all: server client-sync

server: server.8 server-main.8
	$(LD) $(GLFLAGS) -o $@ server-main.8

clean: clean_auto
include ../Makefile

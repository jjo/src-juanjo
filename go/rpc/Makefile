GOCFLAGS=-I.

all: server client-sync

server: server.8 server-main.8
	$(GOL) $(GOLFLAGS) -o $@ $^

include ../Makefile

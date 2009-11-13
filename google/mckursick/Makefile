## Makefile for zocket.c
## Tested on: Linux 2.6, FreeBSD 6.x(dragonfly), OpenBSD 4.3
CFLAGS=-Wall -g
T=zocket.bin.$(OS)
DEST=10.255.255.1 111

## No portable (GNU,BSD) way of doing VAR=<output_from_shellcmd>, wrap
## them by invoking make again
all:
	make OS=`uname -s` all_os
test:
	make OS=`uname -s` test_os
	
all_os: $(T)

setup_pf:
	## FreeBSD: dynload PF module
	-@test -x /sbin/kldload && \
		{ /sbin/kldstat | egrep pf.ko || { kldload pf; sleep 1;};}
	## Enable PF
	-@test -x /sbin/pfctl && \
		sudo /sbin/pfctl -e -f- </dev/null 2>/dev/null;exit 0

test_os: all_os setup_pf
	@ulimit -c 0; [ $(OS) != Linux -a -x /usr/bin/sudo ] && SUDO=sudo;\
		exec $$SUDO ./$(T) $(DEST) | tee test.out.$(OS)

$(T): zocket.c
	$(CC) $(CFLAGS) -o $(@) $(?)

clean:
	rm -fv zocket.bin.*

%.html: %
	c2html -s $(^)

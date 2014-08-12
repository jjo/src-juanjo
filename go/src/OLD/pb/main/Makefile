include $(GOROOT)/src/Make.$(GOARCH)

TARG=main
GOFILES=main.go
DEPS=../http

include $(GOROOT)/src/Make.cmd

cleanall: clean
	make -C ../http clean

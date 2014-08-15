all: out.rst

%.html: %.rst Makefile
	landslide -d $@ $<
%.rst: %.py Makefile
	(cat python-hi.rst; sed 's/^/  /' $<) > $@


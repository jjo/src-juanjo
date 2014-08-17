# Q&D makefile to get mysource.py -> mysource.html
# formatted by landslide
# Use: make mysource.html

%.html: %.rst Makefile
	landslide -d $@ $<
%.rst: %.py Makefile
	(cat python-hi.rst; sed 's/^/  /' $<) > $@


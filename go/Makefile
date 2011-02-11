ifeq ($(GOROOT),)
$(error GOROOT environment var must be set)
endif
include $(GOROOT)/src/Make.inc

SRCS=$(wildcard *.go)
TARGETS_AUTO=$(SRCS:.go=)

test-go-env:
	echo "GOROOT=$${GOROOT?} GOARCH=$${GOARCH?} GOOS=$${GOOS}"

%.$(O): %.go
	$(GC) $(GCFLAGS) $^

%: %.$(O)
	$(LD) $(GLFLAGS) -o $@ $^

%.pretty: %
	gofmt -spaces=true --tabwidth=2 $^ > $@

all_auto: test-go-env $(TARGETS_AUTO)

clean_auto: 
	rm -f $(TARGETS_AUTO) *.8

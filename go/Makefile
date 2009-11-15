GOC=8g
GOL=8l
O_EXT=8

SRCS=$(wildcard *.go)
TARGETS_AUTO=$(SRCS:.go=)

test-go-env:
	echo "GOROOT=$${GOROOT?} GOARCH=$${GOARCH?} GOOS=$${GOOS}"

%.$(O_EXT): %.go
	$(GOC) $^

%: %.$(O_EXT)
	$(GOL) -o $@ $^

%.pretty: %
	gofmt -spaces=true --tabwidth=2 $^ > $@

all_auto: test-go-env $(TARGETS_AUTO)

clean_auto: 
	rm -f $(TARGETS_AUTO)

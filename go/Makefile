GOC=8g
GOL=8l
O_EXT=8

SRCS=$(wildcard *.go)
TARGETS=$(SRCS:.go=)

all: test-go-env $(TARGETS)

test-go-env:
	echo "GOROOT=$${GOROOT?} GOARCH=$${GOARCH?} GOOS=$${GOOS}"

%.$(O_EXT): %.go
	$(GOC) $^

%: %.$(O_EXT)
	$(GOL) -o $@ $^

%.pretty: %
	gofmt -spaces=true --tabwidth=2 $^ > $@

clean: $(TARGETS)
	rm -f $^	

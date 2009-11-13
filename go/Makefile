GOC=8g
GOL=8l
O_EXT=8

%.$(O_EXT): %.go
	$(GOC) $^

%: %.$(O_EXT)
	$(GOL) -o $@ $^

%.pretty: %
	gofmt -spaces=true --tabwidth=2 $^ > $@

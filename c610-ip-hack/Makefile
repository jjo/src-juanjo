TEST_PHONE=4234000
all:

test:
	env REQUEST_URI="/api/siemens?command=get%5flist&type=pb&prid=0&fn=%2a&ln=%2a&ct=%2a&st=%2a&hm=$(TEST_PHONE)&nr=%2a&mb=%2a&sip=%2a&zc=%2a&prid=0&lang=1&first=1&count=1&mac=7C2F8010123C&reqsrc=auto&limit=204" src/api/siemens

show_test_url:
	@echo 'http://tel.search.ch/api/siemens?command=get_list&type=pb&prid=0&fn=%2a&ln=%2a&ct=%2a&st=%2a&hm=$(TEST_PHONE)&nr=%2a&mb=%2a&sip=%2a&zc=%2a&prid=0&lang=1&first=1&count=1&mac=7C2F801E8B7C&reqsrc=auto&limit=204'

install: 
	test -n "$(HOST)" && exit 0 || echo "Missing dst HOST, use: make $@ HOST=a.b.c.d"; exit 1
	rsync --exclude '.*' -vaP src/ root@$(HOST):/www/jjo/
	ssh root@$(HOST) ln -s /www/jjo/siemens-hack.init /etc/rc.d/S99siemenshack

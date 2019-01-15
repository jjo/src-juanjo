sudo tar -C / -zxvf ${1:?missing file.tar.gz} --xform=s,kubernetes/node,/usr, --show-transformed kubernetes/node/bin/

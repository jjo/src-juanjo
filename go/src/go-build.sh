export GOPATH=/home/jjo/src/juanjo/go
dir=${1:?missing directory below $GOPATH/src}
echo GOPATH=$GOPATH
set -x
OUT=~/go-bin/${dir#*/}
go build -o ${OUT} ${dir?} && ls -l ${OUT}

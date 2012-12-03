#!/bin/bash -x
find . -printf "%s %p\n" |./test-find.szl -table_output t /dev/stdin
find . -printf "%s %p\n" |./test-find.szl /dev/stdin

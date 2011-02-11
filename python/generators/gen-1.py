#!/usr/bin/python2.5

import os
import fnmatch
import gzip
import bz2

def gen_find(filepat,top):
  for path, dirlist, filelist in os.walk(top):
    for name in fnmatch.filter(filelist,filepat):
      yield os.path.join(path,name)

def gen_open(filenames):
  for fname in filenames:
    if fname.endswith('.gz'):
      yield(gzip.open(fname))
    elif fname.endswith('.bz'):
      yield(bz2.BZ2File(fname))
    else:
      yield(open(fname))

def gen_cat(files):
  for file in files:
    for line in file:
      yield(line)

def gen_grep(lines):


filenames=gen_find('*.log*', '/var/log')
files=gen_open(filenames)
lines=gen_cat(files)


for line in lines:
  print line,

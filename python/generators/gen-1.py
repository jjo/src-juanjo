#!/usr/bin/python

import os
import fnmatch
import gzip
import bz2
import re

def gen_find(filepat,top):
  for path, dirlist, filelist in os.walk(top):
    for name in fnmatch.filter(filelist,filepat):
      yield os.path.join(path,name)

def gen_open(filenames):
  for fname in filenames:
    try:
      if fname.endswith('.gz'):
        yield(gzip.open(fname))
      elif fname.endswith('.bz'):
        yield(bz2.BZ2File(fname))
      else:
        yield(open(fname))
    except IOError:
      continue

def gen_cat(files):
  for file in files:
    for line in file:
      yield(line)

def gen_grep(lines, pattern):
  regex = re.compile(pattern)
  for line in lines:
    if regex.match(line):
      yield(line)

filenames=gen_find('*.log*', '/var/log')
files=gen_open(filenames)
lines=gen_cat(files)
patt=r'.*jjo\b'
matches=gen_grep(lines, patt)

for line in matches:
  print line,

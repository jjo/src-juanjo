#!/usr/bin/python

"""Do grep thru /var/log logfiles, first argument is pattern to match"""
import os
import fnmatch
import gzip
import bz2
import re
import getopt
import sys

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

def main(args=None):

  if args is None:
    args = sys.argv[1:]
  try:
    opts, args = getopt.getopt(args, "-h",
                              ["help"])

  except getopt.error, err:
    print err
    print "use -h/--help for cmdlien help"
    return 255

  for o,a in opts:
    if o in ("-h", "--help"):
      print __doc__,
      return 0

  patt = '.*%s' % args[0]
  fileroot = args[1]
  filepatt = '*.log*'
  try:
    filepatt = args[2]
  except IndexError:
    pass

  filenames=gen_find(filepatt, fileroot)
  files=gen_open(filenames)
  lines=gen_cat(files)
  matches=gen_grep(lines, patt)

  for line in matches:
    print line,

if __name__ == '__main__':
    sys.exit(main())

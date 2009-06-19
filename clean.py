#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import optparse

def removeFiles(file_list):
  for f in file_list:
    print '  clean %s' % f
    os.remove(f)

def cleandir(dir, suffix):
  print 'start clean %s' % dir
  file_list = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir,f))]
  file_list = [os.path.join(dir, f) for f in file_list if os.path.splitext(f)[1] in suffix]
  removeFiles(file_list)
  dir_list = [os.path.join(dir, f) for f in os.listdir(dir) if os.path.isdir(os.path.join(dir, f))]
  for d in dir_list:
    if not d.endswith('.svn'):
      cleandir(d, suffix)

def cleantmp(tmp_dir):
  print 'start clean tmp files'
  tmpfiles = [f for f in os.listdir(tmp_dir) if os.path.isfile(os.path.join(tmp_dir,f))]
  file_list = [os.path.join(tmp_dir, f) for f in tmpfiles]
  removeFiles(file_list)

def main():
  # args and options init
  parser = optparse.OptionParser(usage='%prog [options] site')
  parser.add_option('-t', '--temp', action="store_true", dest='tmp', default=False,
                    help='Clean tmp files')
  options, args = parser.parse_args()

  clean_suffix = ['.pyc', '.swp']
  root_dir = os.getcwd()

  if options.tmp:
    cleantmp(os.path.join(root_dir, "tmp"))

  cleandir(root_dir, clean_suffix)

if __name__ == '__main__':
  sys.exit(main())


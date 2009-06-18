#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# author: cswenye@gmail.com                                
#

import os
import sys
import optparse

from UserDict import UserDict

from math import log

dic_path = "/home/cswenye/sadke/data/sogou_utf8.dic"

class IDFInfo(UserDict):
  "store idf info from dic"
  def __init__(self, dict=None):
    UserDict.__init__(self)
    if dict:
      self.rebuild(dict)
  
  def rebuild(self, dic_name):
    self.clear()
    sum = 1000000000
    df = file(dic_name, "r")
    while True:
      word_info = df.readline()
      if not word_info:
        break
      infos = word_info.split()
      word = str(infos[0])
      freq = float(infos[1])
      self[word] = float(log(sum*1.0/freq))
    df.close()
  
  def __getitem__(self, key) :
    if self.data.has_key(key) :
      return self.data[key]
    else :
      return 0

def main():
  parser = optparse.OptionParser(usage='%prog [options] [WORD1 WORD2 ...]')
  parser.add_option('-f', '--file', dest='input_file',
                    help='Input filename')

  options, args = parser.parse_args()
  words = args[:]

  idft = IDFInfo(dic_path)

  if words:
    print '>>>>>>>>>>>>>>>>>>'
    print 'The idf info are'
    for w in words :
      print '  %s : %lf' % (w, idft[w])

  print "Input any words you want to get it's idf info, enter directly to exit."
  while True:
    word = raw_input("> ")
    if not word:
      break
    print '--> idf("%s"): %lf' % (word, idft[word])

  return 0

if __name__ == '__main__':
  sys.exit(main())
else:
  idf = IDFInfo(dic_path)


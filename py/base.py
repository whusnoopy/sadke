#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# author: cswenye@gmail.com

import logging
import time

def stringToSeconds(s):
  return time.mktime(time.strptime(s, '%Y-%m-%d %H:%M'))

def LOGGER():
  log = logging.getLogger(__name__)
  log.setLevel(logging.INFO)
  formatter = logging.Formatter('%(asctime)s [%(levelname)s]%(filename)s:'
                                '%(lineno)d: %(message)s', '%m-%d,%H:%M:%S')

  # Console Logger
  ch = logging.StreamHandler()
  ch.setLevel(logging.INFO)
  ch.setFormatter(formatter)
  log.addHandler(ch)

  return log

if __name__ == '__main__' :
  print 'This is a help module, and it exited'
else :
  logger = LOGGER()
  root_dir = '/home/cswenye/sadke/'


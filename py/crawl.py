#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# author: cswenye@gmail.com                                

import os
import sys
import optparse
import urllib2

from base import logging

def crawlPage(url, dir = "/tmp/", max_pagenum = 10):
  filelist = []
  # get web page, translate it to unicode and save it as a local file
  filename = dir + url[url.find('thread-'):]
  if not getUrlAsFile(url, filename):
    return []

  filelist.append(filename)

  # if there is a multi pages topic, get the after pages, and extract them
  pages = checkMultiPage(filename)
  if (pages > 1):
    if pages > max_pagenum:
      pages = max_pagenum
    for page_index in range(2, pages + 1):
      current_url = url[:url.find("-1-")] + "-%d-1.html" % page_index
      filename = dir + current_url[current_url.find('thread-'):]
      if getUrlAsFile(current_url, filename):
        filelist.append(filename)

  return filelist

def getUrlAsFile(url, filename, recrawl = False):
  # avoid re-crawl, if need update, remove the following line
  if os.path.exists(filename) and not recrawl:
    return True
  try:
    wp = urllib2.urlopen(url)
    wp_content = wp.read()
    decode_content = wp_content.decode('gbk')
    f = file(filename, "w")
    f.write(decode_content.encode('utf-8'))
    f.close()
  except UnicodeDecodeError:
    logger.error("Can't decode page %s" % url)
    return False
  except:
    logger.error("Unknown Error during crawl %s" % url)
    return False

  return True

def checkMultiPage(filename):
  f = file(filename, "r")
  content = f.read()
  f.close()
  start_point = content.find('class="p_pages">&nbsp;1/')
  if start_point != -1:
    start_point += 24
    end_point = content.find('&nbsp;', start_point)
    num = content[start_point:end_point]
    return int(num)
  else:
    return 0

def main():
  parser = optparse.OptionParser(usage='%prog [options] FILE')
  
  options, args = parser.parse_args()

  if len(args) < 1:
    parser.error('Url to crawl not provided.')
  elif len(args) > 1:
    parser.error('Only one url may be specified.')

  crawlPage(args[0])

  return 0

if __name__ == '__main__':
  sys.exit(main())


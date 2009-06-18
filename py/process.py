#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# author: cswenye@gmail.com

import os
import sys
import optparse

from base import logger
from crawl import crawlPage
from extract import extractPage
from adsgen import genUpdateAds
from utilxml import outputXmlAdsFile

def main():
  # args and options init
  parser = optparse.OptionParser(usage='%prog url')
  options, args = parser.parse_args()

  # the input file process
  if len(args) < 1:
    parser.error('Url to process not provided.')
  elif len(args) > 1:
    parser.error('Only one url may be specified.')

  url = args[0]
  work_dir = "/home/cswenye/sadke/tmp/"
  thread = url[url.find('thread-'):]
  file_path = os.path.join(work_dir, thread)
  output_file_path = os.path.join(work_dir, "adke.xml")

  # Crawl pages from internet
  print 'crawl...'
  filelist = crawlPage(url, work_dir)

  if not filelist:
    logger.error("Can't crawl url '%s'" % url)
    return -1
  print 'ok!'
  logger.info("crawl '%s' as %s" % (url, ",".join(filelist)))

  # Extract posts
  print 'extract...'
  posts = []
  for f in filelist:
    posts = extractPage(f, posts)

  if not posts:
    logger.error('Extract no post from %s' % url)
    return -1
  print 'ok!'
  logger.info('Read %d posts from %s' % (len(posts), file_path))

  # Gen ads
  print 'gen ads...'
  ads = genUpdateAds(posts)

  print 'ok!'
  logger.info("gen ads finish, write into %s" % output_file_path)
  outputXmlAdsFile(output_file_path, url, posts, ads)

  return 0

if __name__ == "__main__":
  sys.exit(main())


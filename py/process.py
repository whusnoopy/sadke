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
from utilxml import readXmlFile
from utilxml import outputXmlAdsFile

def main():
  # args and options init
  parser = optparse.OptionParser(usage='%prog [OPTIONS] [url]')
  parser.add_option('-d', '--work_dir', dest='work_dir',
                    help='Work dictionary, or will use /home/cswenye/sadke/tmp/ defaultly')
  parser.add_option('-f', '--file', dest='file',
                    help='process html/xml file on disk')
  parser.add_option('-r', '--refresh', action="store_true", dest='refresh', default=False,
                    help='Refresh each page')
  options, args = parser.parse_args()


  if options.work_dir:
    work_dir = os.path.abspath(options.work_dir)
  else:
    work_dir = "/home/cswenye/sadke/tmp/"
  output_file_path = os.path.join(work_dir, "adke.xml")

  url = ""
  if len(args) > 1:
    parser.error('Only one url may be specified.')
  elif len(args) < 1:
    if not options.file:
      parser.error('Url or file to process not provided.')
    elif options.file.endswith(".html"):
      posts = extractPage(options.file)
    elif options.file.endswith(".xml"):
      url, posts = readXmlFile(options.file)
    else:
      parser.error('File to process not supported.')
  else:
    url = args[0]
    # Crawl pages from internet
    filelist = crawlPage(url, work_dir, options.refresh)

    if not filelist:
      logger.error("Can't crawl url '%s'" % url)
      return -1
    logger.info("crawl '%s' as %s" % (url, ",".join(filelist)))
    # Extract posts

    print 'extract...'
    posts = []
    for f in filelist:
      posts = extractPage(f, posts)

  # check extract
  if not posts:
    logger.error('Extract no post')
    return -1
  logger.info('Read %d posts successful' % len(posts))

  # Gen ads
  ads = genUpdateAds(posts)

  logger.info("gen ads finish, write into %s" % output_file_path)
  outputXmlAdsFile(output_file_path, url, posts, ads)

  return 0

if __name__ == "__main__":
  sys.exit(main())


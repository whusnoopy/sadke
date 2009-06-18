#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# author: cswenye@gmail.com

import os
import sys
import time
import optparse

sys.path.append("/home/cswenye/sadke/py/")

from base import logger
from crawl import crawlPage
from extract import extractPage
from adsgen import genUpdateAds
from utilxml import outputXmlAdsFile

def genListHtml(filelist, ref_only, strong_ref):
  dir_path = '/home/cswenye/adke/data/'
  newl = 10
  count = 0
  ll = []
  fl = []
  fl.append('<table><tbody>')
  for t in filelist:
    file_path = os.path.join(dir_path, t)
    if not suitable(file_path, ref_only, strong_ref):
      continue
    ll.append(file_path)
    if count % newl ==0:
      fl.append('<tr>')
    count += 1
    fl.append('<td><a href="demo.php?doc=%s&p=30" target="_blank">%s</a><td>' % (t, t[7:t.find('-',7)]))
    if count % newl == 0:
      fl.append('</tr>')

  ll.append("")
  if count % newl != 0:
    fl.append('</tr>')
  fl.append('</tbody></table>')

  print 'listed files on %s: %d' % (time.strftime('%Y-%m-%d %H:%M:%S'), count)

  return fl, ll


def main():
  # args and options init
  parser = optparse.OptionParser(usage='%prog [options] site')
  parser.add_option('-d', '--work_dir', dest='work_dir',
                    help='Output list filename, or will use /home/cswenye/snoopy/adke/xmllist defaultly')
  parser.add_option('-r', '--refresh', action="store_true", dest='refresh', default=False,
                    help='Refresh each page')
  options, args = parser.parse_args()

  # the input dir process
  if len(args) < 1:
    site = "http://bbs.dospy.com"
  elif len(args) > 1:
    parser.error('Only one dir may be specified.')
  else:
    site = args[0]

  if options.work_dir:
    work_dir = os.path.abspath(options.work_dir)
  else:
    work_dir = "/home/cswenye/sadke/tmp/"

  print 'start to process site %s' % site

  for url in thread_list:

    thread = url[url.find('thread-'):url.find('.html')]
    output_file_path = os.path.join(work_dir, thread, ".xml")

    filelist = crawlPage(url, work_dir, options.refresh)
    if not filelist:
      continue

    posts = []
    for f in filelist:
      posts = extractPage(f, posts)
    if not posts:
      continue

    ads = genUpdateAds(posts)

    outputXmlAdsFile(output_file_path, url, posts, ads)

  print 'process site %s finish' % site

  return 0


if __name__ == "__main__":
  sys.exit(main())


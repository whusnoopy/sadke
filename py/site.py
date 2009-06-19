#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# author: cswenye@gmail.com

import os
import sys
import time
import optparse

from base import logger
from crawl import crawlPage
from crawl import crawlSite
from extract import extractPage
from adsgen import genUpdateAds
from utilxml import readXmlFile
from utilxml import outputXmlAdsFile


def genHtml(filelist, work_dir):
  count = 0
  fl = []
  fl.append('<table><tbody>')
  fl.append('<tr><th width="800">topic</td><th width="96">posts</th></tr>')
  for t in filelist:
    count += 1
    if count % 2:
      fl.append('<tr class="otr">')
    else:
      fl.append('<tr class="etr">')
    file_path = os.path.join(work_dir, t[0])
    if t[2] > 30:
      fl.append('<td><a href="demo.php?doc=%s&p=20" target="_blank">%s</a><span class="hot">Hot!</span></td><td><b>%s</b></td>' % (file_path, t[1], t[2]))
    else:
      fl.append('<td><a href="demo.php?doc=%s&p=20" target="_blank">%s</a></td><td>%s</td>' % (file_path, t[1], t[2]))
    fl.append('</tr>')

  fl.append('</tbody></table>')

  return '\n'.join(fl)

def main():
  # args and options init
  parser = optparse.OptionParser(usage='%prog [options] site')
  parser.add_option('-d', '--work_dir', dest='work_dir',
                    help='Work dictionary, or will use /home/cswenye/adke/ defaultly')
  parser.add_option('-r', '--refresh', action="store_true", dest='refresh', default=False,
                    help='Refresh each page')
  parser.add_option('-g', '--regen_ads', action="store_true", dest='regen', default=False,
                    help='Re-generate ads')
  options, args = parser.parse_args()

  # the input dir process
  if len(args) < 1:
    site = "http://bbs.dospy.com/"
  elif len(args) > 1:
    parser.error('Only one site may be specified.')
  else:
    site = args[0]

  if options.work_dir:
    work_dir = os.path.abspath(options.work_dir)
  else:
    work_dir = os.path.join("/home/cswenye/adke/", ((site.split('/'))[2].split('.'))[1])

  print 'start to process site %s to %s' % (site, work_dir)

  forum_list_file = os.path.join(work_dir, "forumlist")
  thread_list_file = os.path.join(work_dir, "listofthreads")
  html_file = os.path.join(work_dir, "list.html")
  if os.path.exists(thread_list_file) and not options.refresh:
    itf = file(thread_list_file, "r");
    tlist = itf.readlines()
    thread_list = [t[:-1] for t in tlist]
    itf.close()
  else:
    forum_list = []
    if os.path.exists(forum_list_file):
      iff = file(forum_list_file, "r");
      flist = iff.readlines()
      forum_list = [t[:-1] for t in flist]
      iff.close()
    thread_list = crawlSite(site, forum_list)
    liststr = "\n".join(thread_list)
    otf = file(thread_list_file, 'w')
    otf.write(liststr)
    otf.close()

  count = 0
  filelist = []
  for t in thread_list:
    # count += 1

    url = site + t
    thread = (t.split('.'))[-2]
    output_file_path = os.path.join(work_dir, "%s.xml" % thread)

    if os.path.exists(output_file_path):
      try:
        posts = readXmlFile(output_file_path)
      except:
        print sys.exc_info()
      if not options.regen:
        logger.info('%d/ already gen %s, skip' % (count, output_file_path))
        singleline = (output_file_path, posts[0]['title'], len(posts))
        filelist.append(singleline)
        continue
      else:
        logger.info('%d/ crawled %s, regen to %s' % (count, thread, output_file_path))
    else:
      logger.info('%d/ get %s and gen ads to %s' % (count, thread, output_file_path))
      # crawl
      crawlfilelist = crawlPage(url, work_dir, options.refresh, 2, 4)
      if not crawlfilelist:
        logger.info('Crawl %s failed, skip' % url)
        continue
      # extract
      posts = []
      for f in crawlfilelist:
        posts = extractPage(f, posts)
      if not posts:
        logger.info('Extract %s failed, skip' % f)
        continue
    # gen ads
    ads = genUpdateAds(posts)
    # output
    outputXmlAdsFile(output_file_path, url, posts, ads)
    # append html
    singleline = (output_file_path, posts[0]['title'], len(posts))
    filelist.append(singleline)

  # write html file
  if filelist:
    hf = file(html_file, 'w')
    htmlstr = genHtml(filelist, work_dir)
    hf.write(htmlstr)
    hf.close

  print 'process site %s finish' % site

  return 0


if __name__ == "__main__":
  sys.exit(main())


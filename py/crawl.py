#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# author: cswenye@gmail.com                                

import os
import sys
import optparse
import urllib2

from base import logger


def crawlPage(url, dest="/tmp/", refresh=False, max_pagenum=10):
  filelist = []

  filename = dest + url[url.find('thread-'):]
  if os.path.exists(filename) and not recrawl:
    for page_index in range(1, max_pagenum):
      filename = dest + "%s-%d-1.html" % (url[url.find('thread-'):url.find("-1-")], page_index)
      print filename
      if os.path.exists(filename):
        filelist.append(filename)
      else:
        return filelist

  content = getUrl(url)
  if not content:
    return filelist

  f = file(filename, "w")
  f.write(content)
  f.close
  filelist.append(filename)

  # if there is a multi pages topic, get the after pages, and extract them
  start_point = content.find('class="p_pages">&nbsp;1/')
  if start_point != -1:
    start_point += 24
    end_point = content.find('&nbsp;', start_point)
    pages = int(content[start_point:end_point])
  else:
    pages = 1

  if pages > max_pagenum:
    pages = max_pagenum
  for page_index in range(2, pages + 1):
    current_url = url[:url.find("-1-")] + "-%d-1.html" % page_index
    wp_content = getUrl(current_url)
    filename = dest + current_url[current_url.find('thread-'):]
    f = file(filename, "w")
    f.write(wp_content)
    f.close()
    filelist.append(filename)

  return filelist


def crawlSite(site):
  threads = []

  content = getUrl(site)
  if not content:
    return threads

  forum_list = re.findall(ur'forum-[0-9]{1,3}-1\.html', content)

  for forum in forum_list :
    forum_url = site + forum
    content = getUrl(forum_url)
    if not content:
      return threads

    content = content[content.find("论坛主题"):]
    threads.extend([t[t.find("thread"):]
                   for t in re.findall(ur'<td class="f_folder"><a href="thread-[0-9]{1,10}-1-1\.html', content)])

  return threads


def getUrl(url):
  try:
    wp = urllib2.urlopen(url)
    wp_content = wp.read()
    wpcs = wp_content.find('charset=') + 8
    wpct = wp_content.find('"', wpcs)
    wp_coding = wp_content[wpcs:wpct]
    content = wp_content.decode(wp_coding)
    return content.encode('utf-8')
  except UnicodeDecodeError:
    logger.error("Can't decode page %s" % url)
    return False
  except:
    logger.error("Unknown Error during crawl %s" % url)
    return False

  return True


if __name__ == '__main__':
  print 'This is a help module'


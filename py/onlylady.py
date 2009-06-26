#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# author: cswenye@gmail.com

import os
import sys
import re
import optparse
import urllib2
import time

from pymmseg import mmseg
mmseg.dict_load_defaults()

from base import logger
from adsgen import genUpdateAds
from utildospy import grepLastEdit, grepHtmlTag, convertHtmlChar, mergeBlankLines
from utilxml import readXmlFile
from utilxml import outputXmlAdsFile


# Global settings
site_url = "http://bbs.onlylady.com/"
work_dir = "/home/cswenye/adke/onlylady/"


def getUrl(url):
  try:
    wp = urllib2.urlopen(url)
    wp_content = wp.read()
    content = wp_content.decode('gbk')
    return content.encode('utf-8')
  except UnicodeDecodeError:
    logger.error("Can't decode page %s" % url)
    return False
  except:
    logger.error("Unknown Error during crawl %s" % url)
    return False


def detectNextPost(page_content, pos=0):
  post_start = page_content.find('<!--楼层头部信息开始-->', pos)
  if post_start < 0:
    return "", pos

  post_end = page_content.find('<!--楼层正文结束-->', post_start)
  post = page_content[post_start:post_end]

  return post, post_end

def detectPosterId(post_content):
  poster_start = post_content.find('<strong>') + 8
  poster_end = post_content.find('</strong>')
  id = post_content[poster_start:poster_end]

  return id, poster_end

def splitQuotes(body_content):
  quote_start = body_content.find('QUOTE:</div>')
  if quote_start == -1:
    quotes = []
    return body_content, []

  quote = {}
  quote_end = body_content.find('</div><br />')
  quote_content = body_content[quote_start+12:quote_end]

  ids = quote_content.find('<i>') + 3
  idt = quote_content.find('</i>', ids)
  quote['id'] = quote_content[ids:idt]

  qds = idt + 9
  qdt = qds + 16
  quote['date'] = quote_content[qds:qdt]

  qbs = quote_content.find('<br />', qdt) + 6
  body = quote_content[qbs:]
  body = grepHtmlTag(body)
  body = convertHtmlChar(body)
  body = mergeBlankLines(body)
  quote['body'] = body

  body = body_content[quote_end:]
  return body, [quote]

def detectBodyAndQuotes(post_content, pos=0):
  body_start = post_content.find('<!--楼层正文开始-->', pos)
  body_start = post_content.find('<tr><td>', body_start)
  body_end = post_content.find('</td></tr>', body_start)
  body_content = post_content[body_start:body_end]

  body_content, quotes = splitQuotes(body_content)
  body_content = grepLastEdit(body_content)
  body_content = grepHtmlTag(body_content)
  body_content = convertHtmlChar(body_content)
  body_content = body_content.replace('\r', '')
  body_content = mergeBlankLines(body_content)

  return body_content, quotes, body_end

def detectNoAndDateTime(post_content, pos):
  time_start = post_content.find('<span class="time">', pos) + 19
  time_end = post_content.find('</span>', time_start)
  date_time = post_content[time_start:time_end]
  try:
    seconds = time.mktime(time.strptime(date_time, '%Y-%m-%d %H:%M:%S'))
  except Exception, e:
    return "", 0, time_end

  no_start = post_content.find('floor-', time_end) + 6
  no_end = post_content.find("')", no_start)
  post_no = int(post_content[no_start:no_end])

  return post_no, date_time, seconds, no_end
  
def detectPageTitle(page_content):
  ts = page_content.find('<!--帖子标题开始-->')
  if ts == -1:
    return ""

  ts = page_content.find('</span>', ts) + 7
  tt = page_content.find('</div>', ts)
  title = page_content[ts:tt]

  return title

def extractPosts(page_content, posts = []):
  '''Extract a dospy Web Page to posts
  return a posts list that every post is a dictionary like:
    {'no'     : %d,
     'id'     : %s,
     'date'   : %Y-%m-%d %H:%M, # 2009-05-12 14:27
     'time'   : %f, # in seconds
     'title'  : %s,
     'title_tokens' : [token, token, ...], # seged tokens from title
     'body'   : %s,
     'body_tokens'  : [token, token, ...], # seged tokens from body
     'refs'   : [ref, ref, ...]
    }
  and in refs list, a ref is a dictionary like:
    {'no'    : %d,
     'id'    : %s,
     'body'  : %s,
     'tokens': [token, token, ...] # seged tokens from ref body
    }
  '''


  post_content, ppos = detectNextPost(page_content)
  while post_content:
    post = {}

    post['title'] = ""

    # get elements from web page
    post['id'], pos = detectPosterId(post_content)
    post['body'], quotes, pos = detectBodyAndQuotes(post_content, pos)
    post['no'], post['date'], post['time'], pos = detectNoAndDateTime(post_content, pos)

    post['refs'] = []
    for quote in quotes:
      q = {}
      q['id'] = quote['id']
      quote['no'] = post['no']
      for p in posts:
        if p['id'] == quote['id'] and p['date'] == quote['date'][:-3]:
          quote['no'] = p['no']
          break
      q['no'] = quote['no']
      q['body'] = quote['body']
      q['tokens'] = [t.text for t in mmseg.Algorithm(quote['body'])]
      post['refs'].append(q)
    
    # tokenize
    post['title_tokens'] = []
    post['body_tokens'] = [t.text for t in mmseg.Algorithm(post['body'])]

    # Every elements extract already, append this post dictionary to posts
    posts.append(post)
    logger.debug('Got post_%d "%s" post on %f: %s' % \
                  (post['no'], post['title'], post['time'], post['body']))

    # Find next post start
    post_content, ppos = detectNextPost(page_content, ppos)

  if len(posts):
    posts[0]['title'] = detectPageTitle(page_content)
    posts[0]['title_tokens'] = [t.text for t in mmseg.Algorithm(posts[0]['title'])]

  return posts


def processSingleThread(thread):
  if thread.startswith('http'):
    url = thread
    posts = []
    content = getUrl(url)
    if not content:
      logger.error("Can't crawl page %s" % url)
      return -1
    posts = extractPosts(content, posts)
    ps = content.find('<!--页码开始-->')
    pt = content.find('<!--页码结束-->')
    pc = content[ps:pt]
    pages = re.findall('thread-[0-9]{1,7}-[0-9]--\.html', pc)

    print pages

    for p in pages:
      content = getUrl(site_url + p)
      if not content:
        logger.error("Can't crawl page %s" % url)
        return -1
      posts = extractPosts(content, posts)

    output_file_path = os.path.join(work_dir, thread[thread.find('thread'):thread.rfind('.html')] + '.xml')

  elif thread.endswith('html'):
    f = file(thread, "r")
    content = f.read()
    f.close()
    posts = extractPosts(content)
    url = ""

    output_file_path = os.path.join(work_dir, thread[thread.find('thread'):thread.rfind('.html')] + '.xml')

  elif thread.endswith('xml'):
    url, posts = readXmlFile(thread)

    output_file_path = os.path.join(work_dir, thread[thread.find('thread'):])

  else:
    logger.error('unkonw thread %s' % thread)
    return -1

  if not posts:
    logger.error('Extract no post from %s' % thread)
    return -1
  logger.info('Read %d posts' % len(posts))

  # Gen ads
  ads = genUpdateAds(posts)

  logger.info("gen ads finish, write into %s" % output_file_path)
  outputXmlAdsFile(output_file_path, url, posts, ads)
  return 0


def main():
  # args and options init
  parser = optparse.OptionParser(usage='%prog')
  parser.add_option('-f', '--file', dest='file',
                    help='process html/xml file on disk')
  parser.add_option('-s', '--site', dest='site',
                    help='Crawl the whole forum')
  parser.add_option('-r', '--refresh', action="store_true", dest='refresh', default=False,
                    help='Refresh each page')
  options, args = parser.parse_args()

  if options.site:
    forum_url = options.site
    if forum_url.startswith("http"):
      site_content = getUrl(forum_url)
    else:
      f = file(forum_url, "r")
      site_content = f.read()
      f.close()
    if not site_content:
      logger.error("Can't get the forum page %s" % forum_url)
      return -1
    threads = re.findall(ur"thread-[0-9]{1,7}---\.html\'", site_content)
    threads = [site_url + t[:-1] for t in threads]

    for thread in threads:
      processSingleThread(thread)

  elif options.file:
    processSingleThread(options.file)

  elif len(args) < 1:
    parser.error('Url or site to process not provided.')
    return -1

  else:
    processSingleThread(args[0])

  return 0


if __name__ == "__main__":
  sys.exit(main())


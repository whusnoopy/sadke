#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author: cswenye@gmail.com                                

import os
import sys
import optparse

from pymmseg import mmseg
mmseg.dict_load_defaults()

from utildospy import *
from base import logger

def detectSite(content):
  return 'utildospy'

def extractPage(file_path, posts=[]):
  '''Extract a dospy Web Page to posts
  return a posts list that every post is a dictionary like:
    {'no'     : %d,
     'id'     : %d,
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
     'id'    : %d,
     'body'  : %s,
     'tokens': [token, token, ...] # seged tokens from ref body
    }
  '''

  logger.info('Start to extract page %s' % file_path)

  pf = file(file_path, "r")
  page_content = pf.read()
  pf.close()

  site = detectSite(page_content)

  post_content, ppos = detectNextPost(page_content)
  while post_content:
    post = {}
    post['refs'] = []

    # get elements from web page
    post['no'], post['id'], pos = detectPostNo(post_content)
    post['date'], post['time'], pos = detectDateTime(post_content, pos)

    # title and reply_id in head info
    post['title'], reply_id, pos = detectTitleAndReply(post_content, pos)

    if reply_id > 0 and reply_id < post['no']:
      refs = {}
      refs['no'] = reply_id
      refs['id'] = posts[reply_id-1]['id']
      refs['body'] = ""
      refs['tokens'] = []
      post['refs'].append(refs)

    post['body'], quotes, pos = detectBodyAndQuotes(post_content, pos)

    for quote in quotes:
      quote['no'] = post['no']
      for p in posts:
        if p['id'] == quote['id']:
          quote['no'] = p['no']
          break
      quote['tokens'] = [t.text for t in mmseg.Algorithm(quote['body'])]
      post['refs'].append(quote)
    
    # tokenize
    post['title_tokens'] = [t.text for t in mmseg.Algorithm(post['title'])]
    post['body_tokens'] = [t.text for t in mmseg.Algorithm(post['body'])]

    # Every elements extract already, append this post dictionary to posts
    posts.append(post)
    logger.info('Got post_%d "%s" post on %f: %s' % \
                 (post['no'], post['title'], post['time'], post['body']))

    # Find next post start
    post_content, ppos = detectNextPost(page_content, ppos)

  logger.info('Extract %(file_path)s successful.' % locals())
  return posts

def main() :
  parser = optparse.OptionParser(usage='%prog [options] FILE')
  parser.add_option('-o', '--output', dest='output',
                    help='Output filename, or use current time defaultly')
  
  options, args = parser.parse_args()

  if len(args) < 1:
    parser.error('File to extract not provided.')
  elif len(args) > 1:
    parser.error('Only one file may be specified.')

  file_path = args[0]
  posts = extractPage(file_path)

  if options.output:
    pass
  else:
    for p in posts:
      print '========'
      print 'Post %d(%d) "%s" on %s' % (p['no'], p['id'], p['title'], p['date'])
      print '--'
      print p['body']
      print '--'
      for ref in p['refs']:
        print 'to %d(%d): %s' % (ref['no'], ref['id'], ref['body'])
      print '>>>>>>>>'

  return 0

if __name__ == '__main__' :
  sys.exit(main())


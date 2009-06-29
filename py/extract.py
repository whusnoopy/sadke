#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author: cswenye@gmail.com                                

import os
import sys

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

  logger.debug('Start to extract page %s' % file_path)

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
      if reply_id > len(posts):
        refs['id'] = refs['no']
      else:
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
    logger.debug('Got post_%d "%s" post on %f: %s' % \
                  (post['no'], post['title'], post['time'], post['body']))

    # Find next post start
    post_content, ppos = detectNextPost(page_content, ppos)

  logger.debug('Extract %(file_path)s successful.' % locals())
  return posts

if __name__ == '__main__' :
  print 'This is a help module'


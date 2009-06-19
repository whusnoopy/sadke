#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# author: cswenye@gmail.com

import time

from base import logger
from xml.dom import minidom

from pymmseg import mmseg
mmseg.dict_load_defaults()

def convertChar(content, decode=False) :
  html_tags = {
#                '&nbsp;' : ' ',
                '&lt;'   : '<',
                '&gt;'   : '>',
                '&amp;'  : '&',
#                '&quot;' : '"'
              }
  for html_tag, html_char in html_tags.items():
    if decode:
      content = content.replace(html_tag, html_char)
    else:
      content = content.replace(html_char, html_tag)

  return content

def readXmlFile(file_path, number=150):
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
  logger.debug('extract xml file %(file_path)s' % locals())

  xmldoc = minidom.parse(file_path)
  posts = []
  post_nodes = xmldoc.getElementsByTagName('post')

  for post_node in post_nodes:
    post = {}
    post['id'] = int(post_node.getAttribute('id'))
    post['no'] = post['id']
    if post['no'] > number:
      continue

    date_time_node = post_node.getElementsByTagName('date_time')[0]
    if date_time_node.firstChild:
      post['date'] = date_time_node.firstChild.data
      post['time'] = time.mktime(time.strptime(post['date'], '%Y-%m-%d %H:%M'))
    else:
      post['date'] = ""
      post['time'] = 0

    title_node = post_node.getElementsByTagName('title')[0]
    if title_node.firstChild:
      post['title'] = convertChar(title_node.firstChild.data, True).encode('utf-8')
    else:
      post['title'] = ""
    post['title_tokens'] = [t.text for t in mmseg.Algorithm(post['title'])]

    body_node = post_node.getElementsByTagName('body')[0]
    if body_node.firstChild:
      post['body'] = convertChar(body_node.firstChild.data, True).encode('utf-8')
    else:
      post['body'] = ""
    post['body_tokens'] = [t.text for t in mmseg.Algorithm(post['body'])]

    logger.debug('Got post_%d "%s" post on %f: %s' % \
                 (post['no'], post['title'], post['time'], post['body']))

    refs = []
    for ref_node in post_node.getElementsByTagName('ref'):
      ref = {}
      ref['id'] = int(ref_node.getAttribute('id'))
      ref['no'] = ref['id']

      # no refer (ref['id'] == 0)
      if not ref['id']:
        continue

      if ref_node.firstChild:
        ref['body'] = convertChar(ref_node.firstChild.data, True).encode('utf-8')
      else:
        ref['body'] = ""
      ref['tokens'] = [t.text for t in mmseg.Algorithm(ref['body'])]
      
      logger.debug('Got refer to post_%d: %s' % (ref['id'], ref['body']))
      refs.append(ref)

    post['refs'] = refs

    # Every elements extract already, append this post dictionary to posts
    posts.append(post)

  posts.sort(cmp=(lambda x, y: cmp(x['no'], y['no'])))
  return posts

def outputXmlAdsFile(file_path, url, posts, ads):
  '''output ads keywords in sads and pads to a xml file on file_path
  '''

  logger.debug('write ads to xml file %(file_path)s' % locals())
  xmlstr = []
  xmlstr.append('<?xml version="1.0" encoding="utf-8"?>')
  xmlstr.append('<page>\n')

  # origin_page
  xmlstr.append('<origin_page>%s</origin_page>\n' % url)

  # posts
  xmlstr.append('<topic>\n')
  for post in posts:
    xmlstr.append('<post id="%d">' % post['no'])
    xmlstr.append(' <date_time>%s</date_time>' % post['date'])
    xmlstr.append(' <title>%s</title>' % convertChar(post['title']))
    for ref in post['refs']:
      xmlstr.append(' <ref id="%d">%s</ref>' % (ref['no'], convertChar(ref['body'])))
    xmlstr.append(' <body>%s</body>' % convertChar(post['body']))
    xmlstr.append('</post>\n')
  xmlstr.append('</topic>\n')

  # ads
  xmlstr.append('<ads>\n')
  ts = 0
  for tads in ads:
    ts += 1
    xmlstr.append('<tads id="%d">' % ts)
    # ads for whole page without reinforcement
    kws = ["<kw>%s</kw>" % k for k in tads[0]]
    padstr = "".join(kws)
    xmlstr.append(' <banner>%s</banner>' % padstr)
    # ads for whole page with reinforcement
    kws = ["<kw>%s</kw>" % k for k in tads[1]]
    padstr = "".join(kws)
    xmlstr.append(' <sidebar>%s</sidebar>' % padstr)
    # ads for posts
    pno = 0
    for pads in tads[2:]:
      pno += 1
      kws = ["<kw>%s</kw>" % k for k in pads]
      padstr = "".join(kws)
      xmlstr.append(' <pads id="%d">%s</pads>' % (pno, padstr))
    xmlstr.append('</tads>\n')
  xmlstr.append('</ads>\n')

  xmlstr.append('</page>\n')

  ol = []
  for t in xmlstr:
    ol.append(t.decode('utf-8'))
  of = file(file_path, "w")
  ostr = '\n'.join(ol)
  of.write(ostr.encode('utf-8'))
  of.close()

if __name__ == '__main__' :
  print 'This is a help module, and it exited'


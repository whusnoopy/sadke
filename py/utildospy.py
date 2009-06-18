#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author: cswenye@gmail.com                                

import time

from base import logger
from base import stringToSeconds

def detectNextPost(page_content, pos=0):
  post_start = page_content.find('<table border="0" cellspacing="0" cellpadding="4" class="t_msg">', pos)
  if post_start < 0:
    return "", pos

  post_end = page_content.find('</table>', post_start) + 8
  post = page_content[post_start:post_end]

  return post, post_end

def detectPostNo(post_content, pos=0):
  '''extract pno and pid from content at postion pos
  return %(pno)d, %(pid)d, %(npos)d
  '''

  no_start = post_content.find('">#', pos) + 3
  no_end = post_content.find('</a>', no_start)
  pno = int(post_content[no_start:no_end])

  id_start = post_content.find('message', no_end) + 7
  id_end = post_content.find("'", id_start)
  pid = int(post_content[id_start:id_end])

  return pno, pid, id_end

def detectDateTime(post_content, pos):
  '''extract date from content at postion pos
  return %(date)s, %(time)f, %(npos)d # time is time in seconds
  return "", 0, %(npos)d if can't extract time
  '''

  time_start = post_content.find('<div style="padding-top: 4px;">', pos) + 42
  time_end = post_content.find('&nbsp;', time_start)
  t_pos = post_content.find('></a>\n</div>\n', time_end) + 13
  date_time = post_content[time_start:time_end]
  try:
    seconds = time.mktime(time.strptime(date_time, '%Y-%m-%d %H:%M'))
  except Exception, e:
    return "", 0, t_pos

  return date_time, seconds, t_pos

def detectTitleAndReply(post_content, pos):
  '''extract title from content at positon pos
  return %(title)s, %(reply_id)d, %(npos)d
  '''

  title_start = pos + 19
  if post_content[pos:title_start] != '<span class="bold">':
    return "", 0, pos

  title_end = post_content.find('</span>', title_start)
  title = post_content[title_start:title_end]
  title = convertHtmlChar(title)

  if title.startswith('回复 #'):
    if title[8:title.find(' ', 8)].isdigit():
      reply_id = int(title[8:title.find(' ', 8)])
    elif title[8:10].isdigit():
      reply_id = int(title[8:10])
    else:
      reply_id = int(title[8:9])
    title = ""
  else:
    reply_id = 0

  return title, reply_id, title_end

def detectBodyAndQuotes(post_content, pos):
  '''extract title from content at positon pos
  return %(title)s, %(reply_id)d, %(npos)d
  '''

  body_start = post_content.find('class="t_msgfont">', pos)
  if body_start == -1:
    # *** 作者被禁止或删除 内容自动屏蔽 ***
    return "", [], pos

  body_start += 18
  body_end = post_content.find('</div>\r\n<br><font', body_start)
  body_content = post_content[body_start:body_end]

  body_content, quotes = splitQuotes(body_content)
  body_content = grepAttach(body_content)
  body_content = grepLastEdit(body_content)
  body_content = grepHtmlTag(body_content)
  body_content = convertHtmlChar(body_content)
  body_content = body_content.replace('\r', '')
  body_content = mergeBlankLines(body_content)

  return body_content, quotes, body_end

def splitQuotes(content):
  quotes = []
  while True:
    tp = content.find('<div class="msgbody"><div class="msgheader">')
    if tp == -1 :
      break

    quote = {}
    qids = content.find('&amp;pid=', tp)
    if qids == -1:
      # just a text area, not a quote
      content = content[0:tp] + content[tp+44:]
      continue

    qids += 9
    qidt = content.find('&amp;', qids)
    if qidt - qids > 15:
      qidt = content.find('"', qids)
    quote['id'] = int(content[qids:qidt])
    qs = content.find('\r\n', tp) + 2
    qt = content.find('</div></div>', tp)
    quote['body'] = content[qs:qt]
    quotes.append(quote)

    rp = qt + 12
    content = content[0:tp] + content[rp:]

  return content, quotes

def grepAttach(content) :
  attach_tags = [('<div title="menu" class="t_attach"', '</div>', 6), \
                 ('<img src="images/attachicons/', '/>', 2), \
                 ('<a href="http://bbs.dospy.com/attachment.php?aid=', '</a>', 4), \
                 ('<a href="attachment.php', '</a>', 4), \
                 ('<span style="white-space:nowrap" id="attach_', '</span>', 7), \
                 ]

  for atag in attach_tags:
    while True:
      tp = content.find(atag[0])
      if tp == -1:
        break
      rp = content.find('</div></div>', tp)
      if rp == -1:
        rp = content.find('<br', tp)
      if rp == -1:
        rp = content.find(atag[1], tp) + atag[2]
      content = content[:tp] + content[rp:]

  return content

def grepLastEdit(content) :
  while True :
    tp = content.find('[<i> 本帖最后由')
    if tp == -1 :
      break
    rp = content.find('</i>]', tp) + 5
    content = content[0:tp] + content[rp:]
  return content

def grepHtmlTag(content) :
  html_pairs = [('"', '"', 1, 1), \
                ("<", ">", 1, 1)]
  for html_pair in html_pairs:
    pieces = []
    rp = 0
    while True :
      tp = content.find(html_pair[0], rp)
      if tp == -1 :
        break
      pieces.append(content[rp:tp])
      rp = content.find(html_pair[1], tp + html_pair[2])
      if rp == -1:
        tp += html_pair[2]
        continue
      else:
        rp += html_pair[3]
      if len(pieces) > 100:
        pieces.append(content[rp:])
        content="".join(pieces)
        pieces = []
        rp = 0

    pieces.append(content[rp:])
    content = "".join(pieces)

  return content

def convertHtmlChar(content) :
  html_tags = { '&nbsp;' : ' ',
                '&amp;'  : '&',
                '&lt;'   : '<',
                '&gt;'   : '>',
                '&quot;' : '"'
              }
  for html_tag, html_char in html_tags.items() :
    content = content.replace(html_tag, html_char)

  return content

def mergeBlankLines(content):
  while content.find(' \n') != -1:
    content = content.replace(' \n', '\n')
  while content.find('\n\n') != -1:
    content = content.replace('\n\n', '\n')

  sp = (content.startswith('\n')) and 1 or 0
  if content.endswith('\n'):
    content = content[sp:-1]
  else:
    content = content[sp:]
  return content

if __name__ == '__main__':
  print 'This is a help module'


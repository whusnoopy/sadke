#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# author: cswenye@gmail.com

import os
import sys
import optparse

from base import logger


def genHtml(filelist, work_dir):
  count = 0
  fl = []
  fl.append('<table width="100%"><tbody>')
  fl.append('<tr bgColor="#a5d894" height="28px"><th width="80%">Topic</td><th width="20%">Posts</th></tr>')
  for f in filelist:
    count += 1
    if count % 2:
      fl.append('<tr onmouseover="bgColor=\'#ffff40\'" onmouseout="bgColor=\'#e7ffc7\'" bgColor=\'#e7ffc7\'>')
    else:
      fl.append('<tr onmouseover="bgColor=\'#ffff40\'" onmouseout="bgColor=\'#c7f0ef\'" bgColor=\'#c7f0ef\'>')

    ft = file(f, "r")
    fc = ft.read()
    ft.close()
    
    ts = fc.find('<title>') + 7
    tt = fc.find('</title>', ts)
    title = fc[ts:tt]

    ps = fc.rfind('post id="') + 9
    pt = fc.find('"', ps)
    posts = int(fc[ps:pt])
    
    if posts > 30:
      fl.append('<td><a href="demo.php?doc=%s&p=20" target="_blank">%s</a><span class="hot">Hot!</span></td><td><b>%s</b></td>' % (f, title, posts))
    else:
      fl.append('<td><a href="demo.php?doc=%s&p=20" target="_blank">%s</a></td><td>%s</td>' % (f, title, posts))
    fl.append('</tr>')

  fl.append('</tbody></table>')

  return '\n'.join(fl)

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


def main():
  # args and options init
  parser = optparse.OptionParser(usage='%prog [options] site')
  parser.add_option('-d', '--work_dir', dest='work_dir',
                    help='Work dictionary')
  options, args = parser.parse_args()

  if options.work_dir:
    work_dir = options.work_dir
  elif len(args) < 1:
    parser.error('No directory assigned.')
  elif len(args) > 1:
    parser.error('Only one site may be specified.')
  else:
    work_dir = args[0]

  file_list = [f for f in os.listdir(work_dir) if os.path.isfile(os.path.join(work_dir, f))]
  file_list = [os.path.join(work_dir, f) for f in file_list if os.path.splitext(f)[1] == ".xml"]

  fp = os.path.join(work_dir, "list.html")
  f = file(fp, "w")
  fs = genHtml(file_list, work_dir)
  f.write(fs)
  f.close()

  return 0

if __name__ == "__main__":
  sys.exit(main())


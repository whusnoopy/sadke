#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# author: cswenye@gmail.com

from base import logger
from idf import idf

# parameters
alpha = 2     # title additional weight
beta = 0.5    # refer weight
gamma = 0.5   # quote additional weight

def isAdWords(token):
  return True

def isStopWords(token):
  return False

def selectAdWords(scored_tokens, words_number=3, score_limit=1):
  ranked_tokens = sorted(scored_tokens.items(), \
                         cmp=(lambda x, y: cmp(y[1], x[1])))
  ad_words_count = 0
  ad_words = []

  for token, score in ranked_tokens:
    if score < score_limit:
      logger.debug("ad word candidate's score from %(token)s(%(score)f) "
                   "less than limit, skip the following ones" % locals())
      break

    if not isAdWords(token):
      logger.debug('%(token)s(%(score)f) is not ad word, skip it' % locals())
    elif isStopWords(token):
      logger.debug('%(token)s(%(score)f) is stopword, skip it' % locals())
    else:
      ad_words.append(token)
      ad_words_count += 1
      logger.info('%(token)s(%(score)f) is selected as '
                  '%(ad_words_count)d ad word' % locals())

    if ad_words_count == words_number:
      logger.debug("got enough adwords, exit")
      break

  return ad_words

def scoreTokens(tokens, weight=1, scored_tokens={}, scorer=idf):
  '''Help function to generate the tf-idf value for each token in tokens,
  return the sorted tokens dictionary
  '''
  for token in tokens:
    if not scored_tokens.has_key(token):
      scored_tokens[token] = 0
    if not scorer.has_key(token):
      scorer[token] = 0
    scored_tokens[token] += scorer[token]*weight

  return scored_tokens

def mergeScoredTokens(scored_tokens1, scored_tokens2, weight=1):
  merged = {}
  for token, score in scored_tokens1.items():
    if scored_tokens2.has_key(token):
      merged[token] = score + scored_tokens2[token]*weight
    else:
      merged[token] = score
  for token, score in scored_tokens2.items():
    if not scored_tokens1.has_key(token):
      merged[token] = score*weight
  
  return merged

def updateScoredPosts(scored_posts, post):
  for ref in post['refs']:
    logger.debug("Update the post %d's score replied by post %d" % (ref['no'], post['no']))
    # ref['no'] == 0 means it refer to no post before
    if ref['no'] == 0:
      continue
    rs = scored_posts[ref['no']-1]
    if ref['tokens']:
      # part quote
      scored_posts[ref['no']-1] = scoreTokens(ref['tokens'], beta, rs)
    else:
      # refer, consier the body only
      scored_posts[ref['no']-1] = mergeScoredTokens(rs, rs, beta*gamma)
  return scored_posts

def genAds4Post(scored_post, post, scored_posts, ads_num=3):
  '''Generate ad words from scored_posts for a detail post'''

  # original weight
  all_tokens = scored_post

  # other posts' token value
  for ref in post['refs']:
    # ref['no'] == 0 means it refer to no post before
    if ref['no'] == 0:
      continue
    if ref['tokens']:
      # part quote
      all_tokens = scoreTokens(ref['tokens'], beta, all_tokens, scored_posts[ref['no']-1])
    else:
      # refer, consier the body only
      all_tokens = mergeScoredTokens(all_tokens, scored_posts[ref['no']-1], beta*gamma)
     
  ads = selectAdWords(all_tokens, ads_num)
  adskeywords = " ".join(ads)
  logger.info('got ads %s for post %d' % (adskeywords, post['no']))

  return ads

def genAds4Page(scored_posts, ads_num=6):
  '''generate the ads words from already scored posts for the whole page'''

  scored_tokens = {}
  for sp in scored_posts:
    for token, score in sp.items():
      if not scored_tokens.has_key(token):
        scored_tokens[token] = 0
      scored_tokens[token] += score
  ads = selectAdWords(scored_tokens, ads_num)
  adskeywords = " ".join(ads)
  logger.info('got general ads keywords as %(adskeywords)s' % locals())

  return ads

def genUpdateAds(posts):
  '''
  return ads, which is an ads list on each timestamp
    [ads_t1, ads_t2, ...]
    each list node is a list that contains ads words list for whole page
  and each post:
      [ [adsword, adsword, ...], # ads for whole page withno reinforcement
        [adsword, adsword, ...], # ads for whole page with reinforcement
        [adsword, adsword, ...], # ads for post 1
        [adsword, adsword, ...], # ads for post 2
        ...
      ]
  '''

  ads = []
  scored_page = {}
  scored_posts = []

  for np in posts:
    logger.debug('Start to process post %d' % np['no'])
    ads_pt = []

    # add new post into scored page
    scored_page = scoreTokens(np['body_tokens'], scored_tokens=scored_page)
    scored_page = scoreTokens(np['title_tokens'], scored_tokens=scored_page)
    # score new post
    st = {}
    st = scoreTokens(np['body_tokens'], scored_tokens=st)
    st = scoreTokens(np['title_tokens'], weight=alpha, scored_tokens=st)
    # add new scored post into scored posts
    scored_posts.append(st)
    # update old scored posts by new post
    scored_posts = updateScoredPosts(scored_posts, np)

    # gen ads for the whole page without reinforcement (only tf*idf)
    ads_pt.append(selectAdWords(scored_page, 6))
    # gen ads for the whole page
    ads_pt.append(genAds4Page(scored_posts))
    # gen ads for the updated old scored posts
    i = 0
    for sp in scored_posts:
      ads_pt.append(genAds4Post(sp, posts[i], scored_posts))
      i += 1

    ads.append(ads_pt)

  return ads
  

if __name__ == '__main__':
  print 'This is a help module'


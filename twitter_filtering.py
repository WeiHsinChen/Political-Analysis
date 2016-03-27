import json
import pandas as pd
import geocoder
# import matplotlib.pyplot as plt
 
import sys
 
# nickname for every candidate
nick_cand = {}
nick_cand['trump'] = ['donald', 'trump']
nick_cand['cruz'] = ['ted', 'cruz']
nick_cand['kasich'] = ['kasich']
nick_cand['sanders'] = ['bernie', 'sanders']
nick_cand['hillary'] = ['hillary', 'clinton']

tweet_cand = {}
tweet_cand['trump'] = {}
tweet_cand['cruz'] = {}
tweet_cand['kasich'] = {}
tweet_cand['sanders'] = {}
tweet_cand['hillary'] = {}

"""
  sort a tweet by candidate and state
"""
def separate_candidate(tweet):
  cand = None
  count = 0
  for c, ls in nick_cand.items():
    for nick in ls:
      if nick in tweet['text']:
        if count == 0:
          cand = c
          count += 1
        else:
          count += 1
          break
    # tweet contains more than 1 candidate
    if count > 1:
      break

  # tweet contains only 1 candidate
  if count == 1 and cand != None:
    g = geocoder.google(tweet['place']['full_name'])
    if g.state not in tweet_cand[cand]:
      tweet_cand[cand][g.state] = []
    tweet_cand[cand][g.state].append(tweet)



file_name = "dem_tweets.txt"
arguments = sys.argv[1:]
for argument in arguments:
  if argument == "gop":
    file_name = "gop_tweets.txt"
  elif argument in ["dem", "dems"]:
    candidates_filter = "dem_tweets.txt"
 
tweets_data_path = file_name
 
tweets_data = []
tweets_file = open(tweets_data_path, "r")
for line in tweets_file:
  try:
    tweet = json.loads(line)
    if tweet['place'] != None:
      separate_candidate(tweet)
    # tweets_data.append(tweet)
  except:
    continue

print tweet_cand['hillary']
tweets = pd.DataFrame()
 
# ----------------------
tweets['text'] = map(lambda tweet: tweet['text'], tweets_data)
tweets['text'] = map(lambda tweet: tweet['text'], tweets_data)
tweets['lang'] = map(lambda tweet: tweet['lang'], tweets_data)
tweets['country'] = map(lambda tweet: tweet['place']['country'] if tweet['place'] != None else None, tweets_data)
# tweets



# tweets_by_lang = tweets['lang'].value_counts()
# fig, ax = plt.subplots()
# ax.tick_params(axis='x', labelsize=15)
# ax.tick_params(axis='y', labelsize=10)
# ax.set_xlabel('Languages', fontsize=15)
# ax.set_ylabel('Number of tweets' , fontsize=15)
# ax.set_title('Top 5 languages', fontsize=15, fontweight='bold')
# tweets_by_lang[:5].plot(ax=ax, kind='bar', color='red')
# plt.savefig('tweet_by_lang', format='png')
 
# tweets_by_country = tweets['country'].value_counts()
# fig, ax = plt.subplots()
# ax.tick_params(axis='x', labelsize=15)
# ax.tick_params(axis='y', labelsize=10)
# ax.set_xlabel('Countries', fontsize=15)
# ax.set_ylabel('Number of tweets' , fontsize=15)
# ax.set_title('Top 5 countries', fontsize=15, fontweight='bold')
# tweets_by_country[:5].plot(ax=ax, kind='bar', color='blue')
# plt.savefig('tweet_by_country', format='png')
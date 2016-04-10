from time import time
import json
from SentimentAnalysis import SentimentAnalysis
from CategoryAnalysis import CategoryAnalysis
from Visualization import Visualization


"""
  function: predict the sentiment based on text and add a new
            column 'sentiment' on original tweet
"""
def predict_sentiment(tweets_data):
  print 
  print 'predicting sentiment...'
  start = time()

  model_path = 'models/model_NB.pkl'
  sa = SentimentAnalysis()
  sa.load_model(model_path)
  for tweet in tweets_data:
    tweet['sentiment'] = sa.predict_sentiment(tweet['text'])

  print "predicting sentiment: cost %f sec" % (time()-start)


"""
  function: predict the domain based on text and add a new
            column 'domain' on original tweet
"""
def predict_domain(tweets_data):
  print 
  print 'predicting domain...'
  start = time()

  ca = CategoryAnalysis()
  for tweet in tweets_data:
    tweet['domain'] = ca.predict_domain(tweet['text'])

  print "predicting domain: cost %f sec" % (time()-start)

"""
  function: summarize the processed tweets based on sentiment and domain
"""
def summary_state_domain(tweets_data):
  res_state = {}
  res_domain = {}

  for tweet in tweets_data:
    can = tweet['candidate'][0]
    state = tweet['state']
    domains = tweet['domain']
    if can not in res_state:
      res_state[can] = {}
    if can not in res_domain:
      res_domain[can] = {}

    if state not in res_state[can]:
      res_state[can][state] = 0

    for d in domains:
      if d not in res_domain[can]:
        res_domain[can][d] = 0

    if tweet['sentiment'] == 4:
      res_state[can][state] += 1 
      for d in domains:
        res_domain[can][d] += 1 
    elif tweet['sentiment'] == 0:
      res_state[can][state] -= 1 
      for d in domains:
        res_domain[can][d] -= 1 

  return (res_state, res_domain)

# TODO
def parse_tweets():
  tweets_data_path = 'datasets/sample_political_tweets.txt'
  tweets_data = []
  tweets_file = open(tweets_data_path, "r")
  for line in tweets_file:
    try:
      tweet = json.loads(line)
      tweets_data.append(tweet)
    except:
      continue

  predict_sentiment(tweets_data)
  predict_domain(tweets_data)
  with open('datasets/predicted_tweet.txt', 'w') as outfile:
    json.dump(tweets_data, outfile)

  # check what format of file is, based on state or based on candidate
  (sum_state, sum_domain) = summary_state_domain(tweets_data)

  with open('datasets/sum_state.txt', 'w') as outfile:
    json.dump(sum_state, outfile)

  with open('datasets/sum_domain.txt', 'w') as outfile:
    json.dump(sum_domain, outfile)

  print (sum_state, sum_domain)

# TODO
def visualize_tweet_by_state():
  sum_data_path = 'datasets/sum_state.txt'
  sum_data = []
  tweets_file = open(sum_data_path, "r")
  for line in tweets_file:
    try:
      sum_data = json.loads(line)
    except:
      continue
  print sum_data

# TODO
def visualize_tweet_by_domain():
  sum_data_path = 'datasets/sum_domain.txt'
  sum_data = []
  tweets_file = open(sum_data_path, "r")
  for line in tweets_file:
    try:
      sum_data = json.loads(line)
    except:
      continue
  print sum_data

# for test
def check_tweet_on_sentiment():
  predicted_data_path = 'datasets/predicted_tweet.txt'
  predicted_data = []
  tweets_file = open(predicted_data_path, "r")
  for line in tweets_file:
    try:
      predicted_data = json.loads(line)
    except:
      continue
  for tweet in predicted_data:
    print (tweet['text'], tweet['sentiment'])

check_tweet_on_sentiment()
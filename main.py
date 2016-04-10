import json
import SentimentAnalysis
import CategoryAnalysis
import Visualization


def predict_sentiment(tweets_data):
  model_path = 'models/model_NB.pkl'
  sa = SentimentAnalysis()
  sa.load_model(model_path)
  for tweet in tweets_data:
    tweet['sentiment'] = sa.predict_sentiment(tweet['text'])

def predict_domain(tweets_data):
  ca = CategoryAnalysis()
  for tweet in tweets_data:
    tweet['domain'] = ca.predict_domain("trump's social policy is stupid.")

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
      for d in domain:
        res_domain[can][d] += 1 
    elif tweet['sentiment'] == 0:
      res_state[can][state] -= 1 
      for d in domain:
        res_domain[can][d] -= 1 

  return (res_state, res_domain)

if __name__ == "__main__": 
  tweets_data_path = 'sample_political_tweets.txt'
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
  (sum_state, sum_domain) = summary_state_domain(tweets_data)



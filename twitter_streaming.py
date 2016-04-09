# Takes two arguments in any order: 
# max number of tweets retrieved, and candidates to filter by
from __future__ import print_function
import sys
import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from twitter_location_query import get_state_bounding_boxes
import json

# Given list of candidates names, returns name of candidate if 
# tweet is exclusively about them, else returns []
def tweet_contains_exclusive_candidate(tweet, candidates_names_list):
    tweet = tweet.lower()
    number_of_names_contained = 0
    candidate_name = []
    for name_list in candidates_names_list:
        tweet_contains_name = False
        for name in name_list:
            if name in tweet:
                candidate_name = name_list
                tweet_contains_name = True
        if (tweet_contains_name == True):
            number_of_names_contained += 1
    # no names present or too many names present
    if (number_of_names_contained == 0):
        return []
    elif (number_of_names_contained > 1):
        return []
    else:
        return candidate_name[:2]

#Variables that contains the user credentials to access Twitter API 
access_token = "713016345793835009-itRGPior5WpiMa5ELRXpGuC4CrJBJmc"
access_token_secret = "tuxDyQVxU7IdHsJrDsi1Xn9JbDjKwTjglWR5kq7MU9SNA"
consumer_key = "FVL7UVGuBSy9IwRfrDuGd5GQP"
consumer_secret = "5m5JkSZkMvTdUZmZ7wXcCM62Cr4S6Qx7wwK0w2pVE0zAjk7NJK"

cur_num_tweets = 0
max_num_tweets = 1000

# state being currently filtered
cur_state = ''

gop_candidates = [
['donald', 'trump'], 
['cruz'], 
['kasich']]
dem_candidates = [
['bernie', 'sanders', 'bern'], 
['hillary', 'clinton']]
# dem candidates by default
candidates_filter = gop_candidates + dem_candidates

candidates_keywords = []
for list in candidates_filter:
    for name in list:
        candidates_keywords.append(name)

output_file = open('political_tweets.txt','w')

# parse arguments, max tweets and candidate filters
arguments = sys.argv[1:]
for argument in arguments:
    # if integer, set max tweets
    if argument.isdigit() == True:
        max_num_tweets = int(argument)
    else:
        if argument == "gop":
            candidates_filter = gop_candidates
        elif argument in ["dem", "dems"]:
            candidates_filter = dem_candidates
        elif argument in ["all", "both"]:
            candidates_filter = gop_candidates + dem_candidates
        else:
            candidates_filter = gop_candidates + dem_candidates

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        # If tweet does not contains one candidate, do nothing
        data = json.loads(data)
        #print data["text"].lower()
        candidate_name = tweet_contains_exclusive_candidate(data["text"].lower(), candidates_filter)
        if (candidate_name == []):
            return True
        # new formatted tweet
        global cur_state, cur_num_tweets, max_num_tweets, output_file

        tweet_dict = {}
        data["candidate"] = candidate_name
        data["state"] = cur_state

        print(json.dumps(data),file=output_file)

        cur_num_tweets += 1
        print(cur_num_tweets)
        if cur_num_tweets == max_num_tweets:
            return False
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    # Get bounding boxes for states
    #state_bounding_boxes_dict = get_state_bounding_boxes(auth)
    #{'Oklahoma': [-103.0026515, 33.615765, -94.431332, 37.002328], 'Wyoming': [-111.056888, 40.994746, -104.052236, 45.005904], 'New Mexico': [-109.050173, 31.332176, -103.002065, 37.000294], 'Wisconsin': [-92.889433, 42.491921, -86.24955, 47.309715], 'Kansas': [-102.051769, 36.9931101, -94.588081, 40.003282], 'Oregon': [-124.703541, 41.991795, -116.463262, 46.2990779], 'Connecticut': [-73.727776, 40.950918, -71.786994, 42.050588], 'New Hampshire': [-72.557247, 42.6969837, -70.575095, 45.305476], 'West Virginia': [-82.644739, 37.201483, -77.7189303, 40.638802], 'South Carolina': [-83.353955, 32.04683, -78.499301, 35.215449], 'California': [-124.482003, 32.528832, -114.131212, 42.009519], 'Georgia': [-85.605166, 30.355644, -80.742567, 35.000771], 'North Dakota': [-104.048915, 45.935021, -96.554508, 49.000693], 'Florida': [-87.634643, 24.396308, -79.974307, 31.001056], 'Kentucky': [-89.57151, 36.497129, -81.964971, 39.147359], 'Rhode Island': [-71.907259, 41.095834, -71.088567, 42.018808], 'Nebraska': [-104.053515, 39.9997506, -95.30829, 43.001708], 'Ohio': [-84.8203089, 38.403186, -80.518626, 42.327133], 'South Dakota': [-104.05774, 42.479636, -96.43659, 45.945379], 'Colorado': [-109.060257, 36.992427, -102.041524, 41.003445], 'New Jersey': [-75.563587, 38.788657, -73.88506, 41.357424], 'Washington': [-124.848975, 45.543542, -116.915989, 49.0025023], 'North Carolina': [-84.3219475, 33.752879, -75.40012, 36.588118], 'New York': [-79.76259, 40.477383, -71.777492, 45.015851], 'Nevada': [-120.00574, 35.002086, -114.039649, 42.002208], 'Delaware': [-75.7887564, 38.4510398, -74.984165, 39.839007]}

    state_bounding_boxes_dict = {
    #'Massachussetts':[-73.508143, 41.187054, -69.858861, 42.8868241]
    #'Michigan':[-90.4181075, 41.696088, -82.122971, 48.306272]
    #'Wyoming':[-111.056888, 40.994746, -104.052236, 45.005904]}
    'New York':[-79.76259, 40.477383, -71.777492, 45.015851]}
    #'California':[-124.482003, 32.528832, -114.131212, 42.009519]}

    #This line filter Twitter Streams to capture data by the keywords
    #stream.filter(track=candidates_filter)
    #This line filter Twitter Streams to capture data by state
    for state in state_bounding_boxes_dict:
        cur_state = state
        state_bounding_box = state_bounding_boxes_dict[state]
        # convert to integers
        print(cur_state)
        stream.filter(locations=state_bounding_box)
        #stream.filter(track=candidates_keywords)
        # reset count
        cur_num_tweets = 0
    output_file.close()
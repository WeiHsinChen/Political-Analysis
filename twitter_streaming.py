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
import time
import ssl
import random
ssl._create_default_https_context = ssl._create_unverified_context

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
# access_token = "713016345793835009-itRGPior5WpiMa5ELRXpGuC4CrJBJmc"
# access_token_secret = "tuxDyQVxU7IdHsJrDsi1Xn9JbDjKwTjglWR5kq7MU9SNA"
# consumer_key = "FVL7UVGuBSy9IwRfrDuGd5GQP"
# consumer_secret = "5m5JkSZkMvTdUZmZ7wXcCM62Cr4S6Qx7wwK0w2pVE0zAjk7NJK"
 
access_token = "3519287422-aEIFkrNSPrk3YBVCdDoIPERBRQbgAT2paQOvmSy"
access_token_secret = "6HgbwAAnYglKHDCyLDCMwkmiRcOLqI1nMXrOdA0luYaSX"
consumer_key = "TXk7hUXZukYDhqDNl6bT6lJwv"
consumer_secret = "LOnkZSNAWIHcbFdbGB50uvpoTh8qeYWILEXNT695IFDOBcrpv9"

cur_num_tweets = 0
max_num_tweets = 100
min_limit = 30

use_timer = True
initial_time = 0

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

run_real_time = True

candidates_keywords = []
for list in candidates_filter:
    for name in list:
        candidates_keywords.append(name)

output_file = open('datasets/predicted_tweet.txt','a')

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
        elif argument == "realtime":
            run_real_time = True
        elif 'min' in argument:
            argument = argument.strip('min')
            min_limit = int(argument)
time_limit = 60 * min_limit

from SentimentAnalysis import SentimentAnalysis
from CategoryAnalysis import CategoryAnalysis
model_path = 'models/model_NB.pkl'
sa = SentimentAnalysis()
ca = CategoryAnalysis()
if run_real_time == True:
    sa.load_model(model_path)
from subprocess import Popen, PIPE    
map_process = None

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
    '''
    
    Standard output class for straeming tweets.

    '''
    def on_data(self, data):
        '''
        
        Receives streaming tweets in the form of a json formatted string to data.
        Analyzes the data to include only relevant candidates and the sentiment.

        :param data: A json formatted string of tweet metadata

        '''
        # If we've exceeded time limit, quit
        global initial_time
        if ((time.time() - initial_time) > time_limit):
            return False

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
        if run_real_time == True:
            data["sentiment"] = sa.predict_sentiment(data["text"])
            data["domain"] = ca.predict_domain(data["text"])

        print(json.dumps(data),file=output_file)


        cur_num_tweets += 1
        print("# of tweets collected in", cur_state, ":", cur_num_tweets)
        if cur_num_tweets == max_num_tweets:
            return False
        return True

    def on_error(self, status):
        '''
        If any error occurs during streaming process, prints the error status.

        :param status: A string of the error status encountered
        '''
        print(status)


def main():
    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    # Get bounding boxes for states
    #state_bounding_boxes_dict = get_state_bounding_boxes(auth)
    state_bounding_boxes_dict = \
    {'Mississippi': [-91.655009, 30.146096, -88.097889, 34.995968], 'Iowa': [-96.6396669, 40.375437, -90.140061, 43.50102], 'Oklahoma': [-103.0026515, 33.615765, -94.431332, 37.002328], 'Wyoming': [-111.056888, 40.994746, -104.052236, 45.005904], 'Minnesota': [-97.239256, 43.499362, -89.483385, 49.384359], 'Illinois': [-91.51308, 36.970298, -87.019935, 42.508303], 'Arkansas': [-94.61771, 33.004106, -89.644838, 36.499767], 'New Mexico': [-109.050173, 31.332176, -103.002065, 37.000294], 'Indiana': [-88.097892, 37.771743, -84.78458, 41.761368], 'Maryland': [-79.487651, 37.886607, -74.986286, 39.723622], 'Louisiana': [-94.043628, 28.855128, -88.758389, 33.019544], 'Idaho': [-117.243028, 41.987982, -111.0434969, 49.001121], 'Tennessee': [-90.310298, 34.982924, -81.646901, 36.678119], 'Arizona': [-114.818269, 31.3322463, -109.0451527, 37.004261], 'Wisconsin': [-92.889433, 42.491921, -86.24955, 47.309715], 'Michigan': [-90.4181075, 41.696088, -82.122971, 48.306272], 'Kansas': [-102.051769, 36.9931101, -94.588081, 40.003282], 'Utah': [-114.052999, 36.997905, -109.041059, 42.001619], 'Virginia': [-83.67529, 36.540739, -75.16644, 39.466012], 'Oregon': [-124.703541, 41.991795, -116.463262, 46.2990779], 'Connecticut': [-73.727776, 40.950918, -71.786994, 42.050588], 'Montana': [-116.050004, 44.35821, -104.039563, 49.00139], 'New Hampshire': [-72.557247, 42.6969837, -70.575095, 45.305476], 'Texas': [-106.645646, 25.837092, -93.508131, 36.500695], 'West Virginia': [-82.644739, 37.201483, -77.7189303, 40.638802], 'South Carolina': [-83.353955, 32.04683, -78.499301, 35.215449], 'California': [-124.482003, 32.528832, -114.131212, 42.009519], 'Massachusetts': [-73.508143, 41.187054, -69.858861, 42.8868241], 'Vermont': [-73.437741, 42.726853, -71.464604, 45.01666], 'Georgia': [-85.605166, 30.355644, -80.742567, 35.000771], 'North Dakota': [-104.048915, 45.935021, -96.554508, 49.000693], 'Hawaii': [-178.443593, 18.86546, -154.755792, 28.517269], 'Pennsylvania': [-80.519851, 39.719801, -74.689517, 42.516072], 'Florida': [-87.634643, 24.396308, -79.974307, 31.001056], 'Alaska': [-179.231086, 51.175093, 179.859685, 71.434357], 'Kentucky': [-89.57151, 36.497129, -81.964971, 39.147359], 'Rhode Island': [-71.907259, 41.095834, -71.088567, 42.018808], 'Nebraska': [-104.053515, 39.9997506, -95.30829, 43.001708], 'Missouri': [-95.774704, 35.995476, -89.098843, 40.613641], 'Ohio': [-84.8203089, 38.403186, -80.518626, 42.327133], 'Alabama': [-88.473228, 30.144425, -84.888247, 35.008029], 'South Dakota': [-104.05774, 42.479636, -96.43659, 45.945379], 'Colorado': [-109.060257, 36.992427, -102.041524, 41.003445], 'New Jersey': [-75.563587, 38.788657, -73.88506, 41.357424], 'Washington': [-124.848975, 45.543542, -116.915989, 49.0025023], 'North Carolina': [-84.3219475, 33.752879, -75.40012, 36.588118], 'New York': [-79.76259, 40.477383, -71.777492, 45.015851], 'Nevada': [-120.00574, 35.002086, -114.039649, 42.002208], 'Delaware': [-75.7887564, 38.4510398, -74.984165, 39.839007], 'Maine': [-71.084335, 42.917127, -66.885075, 47.459687]}
    state_codes = \
    {'Mississippi': 'MS', 'Oklahoma': 'OK', 'Wyoming': 'WY', 'Minnesota': 'MN', 'Alaska': 'AK', 'Illinois': 'IL', 'Arkansas': 'AR', 'New Mexico': 'NM', 'Indiana': 'IN', 'Maryland': 'MD', 'Louisiana': 'LA', 'Texas': 'TX', 'Iowa': 'IA', 'Wisconsin': 'WI', 'Arizona': 'AZ', 'Michigan': 'MI', 'Kansas': 'KS', 'Utah': 'UT', 'Virginia': 'VA', 'Oregon': 'OR', 'Connecticut': 'CT', 'Tennessee': 'TN', 'New Hampshire': 'NH', 'Idaho': 'ID', 'West Virginia': 'WV', 'South Carolina': 'SC', 'California': 'CA', 'Massachusetts': 'MA', 'Vermont': 'VT', 'Georgia': 'GA', 'North Dakota': 'ND', 'Pennsylvania': 'PA', 'Florida': 'FL', 'Hawaii': 'HI', 'Kentucky': 'KY', 'Rhode Island': 'RI', 'Nebraska': 'NE', 'Missouri': 'MO', 'Ohio': 'OH', 'Alabama': 'AL', 'South Dakota': 'SD', 'Colorado': 'CO', 'New Jersey': 'NJ', 'Washington': 'WA', 'North Carolina': 'NC', 'New York': 'NY', 'Montana': 'MT', 'Nevada': 'NV', 'Delaware': 'DE', 'Maine': 'ME'}
    states = \
    ['California', 'Texas', 'Florida', 'New York', 'Illinois', 'Pennsylvania', 'Ohio', 'Georgia', 'North Carolina', 'Michigan', 'New Jersey', 'Virginia', 'Washington', 'Arizona', 'Massachusetts', 'Indiana', 'Tennessee', 'Missouri', 'Maryland', 'Wisconsin', 'Minnesota', 'Colorado', 'South Carolina', 'Alabama', 'Louisiana', 'Kentucky', 'Oregon', 'Oklahoma', 'Connecticut', 'Iowa', 'Utah', 'Mississippi', 'Arkansas', 'Kansas', 'Nevada', 'New Mexico', 'Nebraska', 'West Virginia', 'Idaho', 'Hawaii', 'New Hampshire', 'Maine', 'Rhode Island', 'Montana', 'Delaware', 'South Dakota', 'North Dakota', 'Alaska', 'Vermont', 'Wyoming']

    # states = []
    # state_bounding_boxes_dict = {
    #'Massachussetts':[-73.508143, 41.187054, -69.858861, 42.8868241]}
    #'Michigan':[-90.4181075, 41.696088, -82.122971, 48.306272]}
    #'Wyoming':[-111.056888, 40.994746, -104.052236, 45.005904]}
    # 'New York':[-79.76259, 40.477383, -71.777492, 45.015851]}
    #'California':[-124.482003, 32.528832, -114.131212, 42.009519]}

    #This line filter Twitter Streams to capture data by the keywords
    #stream.filter(track=candidates_filter)
    #This line filter Twitter Streams to capture data by state

    while True:
        state = random.choice(states)
        cur_state = state
        state_bounding_box = state_bounding_boxes_dict[state]
        # convert to integers
        print(cur_state)
        initial_time = time.time()
        stream.filter(locations=state_bounding_box)
        # output_file.close()
        #stream.filter(track=candidates_keywords)
        # reset count
        if run_real_time == True:
            if map_process != None:
                map_process.terminate()
            map_process = Popen(['python', 'main.py'])
        cur_num_tweets = 0

main()    
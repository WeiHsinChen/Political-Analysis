# only for importing on horton!!!
import sys
sys.path.append("/home/aliradha/eecs549/tweepy")
import tweepy

#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Variables that contains the user credentials to access Twitter API 
access_token = "713016345793835009-itRGPior5WpiMa5ELRXpGuC4CrJBJmc"
access_token_secret = "tuxDyQVxU7IdHsJrDsi1Xn9JbDjKwTjglWR5kq7MU9SNA"
consumer_key = "FVL7UVGuBSy9IwRfrDuGd5GQP"
consumer_secret = "5m5JkSZkMvTdUZmZ7wXcCM62Cr4S6Qx7wwK0w2pVE0zAjk7NJK"

cur_num_tweets = 0
max_num_tweets = 10000

gop_candidates = ['donald', 'trump', 'ted', 'cruz', 'kasich']
dem_candidates = ['bernie', 'sanders', 'hillary', 'clinton']
# dem candidates by default
candidates_filter = dem_candidates

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
            candidates_filter = dem_candidates

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        global cur_num_tweets, max_num_tweets
        cur_num_tweets += 1
        print data
        if cur_num_tweets == max_num_tweets:
            return False
        return True

    def on_error(self, status):
        print status


if __name__ == '__main__':
    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords
    stream.filter(track=candidates_filter)
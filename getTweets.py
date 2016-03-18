import time
from TwitterSearch import *
import geocoder

try:
    tso = TwitterSearchOrder() # create a TwitterSearchOrder object
    tso.set_keywords(['Clinton', 'Sanders']) # let's define all words we would like to have a look for
    # tso.set_language('en') 
    g = geocoder.google('new york');
    tso.set_geocode(g.latlng[0], g.latlng[1], 100, False)
    tso.set_include_entities(True) # and don't give us all those entity information

    # it's about time to create a TwitterSearch object with our secret tokens
    ts = TwitterSearch(
        consumer_key = 'TXk7hUXZukYDhqDNl6bT6lJwv',
        consumer_secret = 'LOnkZSNAWIHcbFdbGB50uvpoTh8qeYWILEXNT695IFDOBcrpv9',
        access_token = '3519287422-aEIFkrNSPrk3YBVCdDoIPERBRQbgAT2paQOvmSy',
        access_token_secret = '6HgbwAAnYglKHDCyLDCMwkmiRcOLqI1nMXrOdA0luYaSX'
     )
    def my_callback_closure(current_ts_instance): # accepts ONE argument: an instance of TwitterSearch
        queries, tweets_seen = current_ts_instance.get_statistics()
        print 'queries', queries, 'tweets_seen', tweets_seen
        # if queries > 0 and (queries % 5) == 0: # trigger delay every 5th query
        #     time.sleep(60) # sleep for 60 seconds

    s = set()
     # this is where the fun actually starts :)
    i = 0
    while True:
        for tweet in ts.search_tweets_iterable(tso, callback=my_callback_closure):
            # if (tweet['id'] in s):
            #     print '----------'
            #     print 'duplicate'
            #     print '----------'
            #     continue
            s.add(tweet['id'])
            print( '@%s tweeted: %s, followers_count: %d' % (tweet['user']['screen_name'].encode('utf-8'), tweet['text'].encode('utf-8'), tweet['user']['followers_count']))
            i += 1
        print i
        time.sleep(200)     
except TwitterSearchException as e: # take care of all those ugly errors if there are some
    print(e)
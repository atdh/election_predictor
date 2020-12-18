# variables that contain the user credential to access twitter api
import tweepy
from tweepy import OAuthHandler
import json


ACCESS_TOKEN = "114045110-LPVjgKBTMaL86tT2zxzzhQIocm2LhJAy8ouTu0qV"
ACCESS_TOKEN_SECRET = "ag66NBTZ6vsXFtVP4jSAmKfUniyIbmh6uYodHOpUFvnfD"
CONUMER_KEY = "ULragai1aU4PrxucV4e8zgavR"
CONSUMER_SECRET = "9exmcK5u4HfnQtaYOOEI3ZW2wyXJzWaps1cks7ETNFwfsR9y1n"

#auth = OAuthHandler(CONUMER_KEY, CONSUMER_SECRET)
# auth.set_access_token(ACCESS_TOKEN, #ACCESS_TOKEN_SECRET)

#api = tweepy.API(auth)


# def process_or_store(tweet):
#    print(json.dumps(tweet))


'''
for status in tweepy.Cursor(api.home_timeline).items(10):
    # Process a single status
    process_or_store(status._json)
'''

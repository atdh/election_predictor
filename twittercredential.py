# variables that contain the user credential to access twitter api
import tweepy
from tweepy import OAuthHandler
import json


ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""
CONUMER_KEY = ""
CONSUMER_SECRET = ""

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

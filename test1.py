import csv
import re
from textblob import TextBlob
import json
from tweepy import StreamListener
import twittercredential
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream


import tweepy
from datetime import datetime

auth = tweepy.OAuthHandler(
    twittercredential.CONUMER_KEY, twittercredential.CONSUMER_SECRET)
auth.set_access_token(twittercredential.ACCESS_TOKEN,
                      twittercredential.ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)
# timeline
'''
tweets = api.home_timeline()
for tweet in tweets:
    print(tweet.text)'''
# get tweet stream and do sentiment analysis

# ~~~~~~~~~~~~~~~~~~
trump = 0
biden = 0

header_name = ['Trump', 'Biden']

with open('sentiment.csv', 'w') as file:
    writer = csv.DictWriter(file, fieldnames=header_name)
    writer.writeheader()


class listener(StreamListener):
    def on_data(self, data):
        raw_tweets = json.loads(data)
        try:
            tweets = raw_tweets['text']

            tweets = ' '.join(
                re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweets).split())

            tweets = ' '.join(re.sub('RT', ' ',   tweets).split())

            blob = TextBlob(tweets.strip())
            global trump
            global biden

            trump_sentiment = 0
            biden_sentiment = 0

            for sent in blob.sentences:
                if "Trump" in sent and "Biden" not in sent:
                    # print(sent.sentiment.polarity)
                    trump_sentiment = trump_sentiment + sent.sentiment.polarity
                else:
                    biden_sentiment = biden_sentiment + sent.sentiment.polarity
                    # print(raw_tweets['text'])

            trump = trump + trump_sentiment
            biden = biden + biden_sentiment

            with open('sentiment.csv', 'a') as file:
                writer = csv.DictWriter(file, fieldnames=header_name)

                info = {
                    "Trump": trump,
                    "Biden": biden
                }

                writer.writerow(info)

            print(tweets)
            print()

        except:
            print('Error')

    def on_error(self, status):
        print(status)


'''
auth = tweepy.OAuthHandler(
    twittercredential.CONUMER_KEY, twittercredential.CONSUMER_SECRET)
auth.set_access_token(twittercredential.ACCESS_TOKEN,
                      twittercredential.ACCESS_TOKEN_SECRET)'''

twitter_stream = Stream(auth, listener())
twitter_stream.filter(track=['Trump', 'Biden'])

import tweepy
import twittercredential
# from twittercredential import auth
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from tweepy import API
from tweepy import Cursor
import numpy as np
import pandas as pd

from textblob import TextBlob
import re

import matplotlib.pyplot as plt

# Twitter CLIENT


class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list

    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets
# TWITTER AUTHENTICATOR


class TwitterAuthenticator():
    def authenticate_twitter_app(self):
        auth = OAuthHandler(twittercredential.CONUMER_KEY,
                            twittercredential.CONSUMER_SECRET)
        auth.set_access_token(twittercredential.ACCESS_TOKEN,
                              twittercredential.ACCESS_TOKEN_SECRET)
        return auth


class TwitterStreamer():
    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()
    # class for straming and processing live tweets

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_authenticator.authenticate_twitter_app()
        stream = Stream(auth, listener)

        # this handles twitter authentication and connection to the twitter streaming api
        stream.filter(track=hash_tag_list)


class TwitterListener(StreamListener):
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try:
            with open('python.json', 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        if status == 420:
            return False
        print(status)


class TweetAnalyzer():
    # functionality for analyzing and categorizing content from tweet

    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def analyze_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))

        if analysis.sentiment.polarity > 0:
            return 1
        elif analysis.sentiment.polarity == 0:
            return 0
        else:
            return -1

    def tweets_to_data_frame(self, tweets):
        df = pd.DataFrame(
            data=[tweet.text for tweet in tweets], columns=['Tweets'])

        df['id'] = np.array([tweet.id for tweet in tweets])

        df['len'] = np.array([len(tweet.text) for tweet in tweets])

        df['date'] = np.array([tweet.created_at for tweet in tweets])

        df['source'] = np.array([tweet.source for tweet in tweets])

        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])

        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])
        return df


if __name__ == "__main__":
    print('hi')

    #twitter_streamer = TwitterStreamer()

    twitter_client = TwitterClient()
    tweet_analyzer = TweetAnalyzer()
    api = twitter_client.get_twitter_client_api()
    tweets = api.user_timeline(screen_name="realDonaldTrump", count=10000)

    # print(dir(tweets[0]))
    # print(tweets[0].id)
    # print(tweets[0].retweet_count)
    df = tweet_analyzer.tweets_to_data_frame(tweets)
    '''
    df['sentiment'] = np.array(
        [tweet_analyzer.analyze_sentiment(tweet) for tweet in df['Tweets']])'''

    # picking positive tweets from tweets
    ptweets = np.array([tweet_analyzer.analyze_sentiment(
        tweet) for tweet in df['Tweets'] if tweet_analyzer.analyze_sentiment(tweet) == 1])

    print("Positive tweets percentage: {} %".format(
        100*len(ptweets)/len(df['Tweets'])))
    # picking negative tweets from tweets
    ntweets = np.array([tweet_analyzer.analyze_sentiment(
        tweet) for tweet in df['Tweets'] if tweet_analyzer.analyze_sentiment(tweet) == -1])

    print("negative tweets percentage: {} %".format(
        100*len(ntweets)/len(df['Tweets'])))

    # picking neurtal tweets
    neutral = np.array([tweet_analyzer.analyze_sentiment(
        tweet) for tweet in df['Tweets'] if tweet_analyzer.analyze_sentiment(tweet) == 0])

    print("neutral tweets percentage: {} %".format(
        100*len(neutral)/len(df['Tweets'])))

    # print(df.head(10))
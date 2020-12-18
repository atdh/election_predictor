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
    def tweets_to_data_frame(self, tweets):
        df = pd.DataFrame(
            data=[tweet.text for tweet in tweets], columns=['Tweets'])
        return df


if __name__ == "__main__":
    print('hi')
    hash_tag_list = ['#Trump2020', '#MAGA', '#maga2020', '#kag',
                     '#makeamericagreatagain',  '#keepamericagreat', '#trumptrain']

    fetched_tweets_filename = 'tweets.json'
    #twitter_streamer = TwitterStreamer()

    twitter_client = TwitterClient()
    tweet_analyzer = TweetAnalyzer()
    api = twitter_client.get_twitter_client_api()
    tweets = api.user_timeline(screen_name="realDonaldTrump", count=20)
    # print(tweets)
    # print(twitter_client.get_user_timeline_tweets(1))
    df = tweet_analyzer.tweets_to_data_frame(tweets)
    df.head(10)
    #twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)
    # print(twitter_client.get_user_timeline_tweets(5))

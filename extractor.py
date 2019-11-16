import tweepy
import json

with open('credentials.json') as creds:
    credentials = json.load(creds)

auth = tweepy.auth.OAuthHandler(credentials["consumer_key"], credentials["consumer_secret"])
auth.set_access_token(credentials["access_token"], credentials["access_secret"])

api = tweepy.API(auth)

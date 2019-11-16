import tweepy as tw
import json

with open('creds.json') as creds:
    credentials = json.load(creds)

auth = tw.auth.OAuthHandler(credentials["consumer_key"], credentials["consumer_secret"])
auth.set_access_token(credentials["access_token"], credentials["access_secret"])

api = tw.API(auth, wait_on_rate_limit=True)
date_since = "2018-10-15"
tweets = tw.Cursor(api.search,
                   geocode="43.17305,-77.62479,120km",
                   lang="en",
                   since=date_since).items(5)

for tweet in tweets:
    print(tweet.created_at, tweet.text, tweet.lang)

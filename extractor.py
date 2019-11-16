import tweepy as tw
import json
import logging


def auth():
    with open('creds.json') as creds:
        credentials = json.load(creds)

    auth = tw.auth.OAuthHandler(credentials["consumer_key"], credentials["consumer_secret"])
    auth.set_access_token(credentials["access_token"], credentials["access_secret"])
    api = tw.API(auth, wait_on_rate_limit=True)
    return api


api = auth()


def get_random_users(geocode="40.68908,-73.95860,200km", n=100, lang="en", date_since="2018-10-15"):
    users_names = set()
    while len(users_names) <= n:
        for tweet in tw.Cursor(
                api.search,
                geocode=geocode,
                lang=lang,
                since=date_since).items(10):
            users_names.add(tweet.user.screen_name)
            logging.info("Got user: " + str(tweet.user.screen_name))
    return list(users_names)


def get_tweets_from_user(user_name, num_tweets):
    return [
        (tweet.text, tweet.entities) for tweet in
        tw.Cursor(api.user_timeline, screen_name=user_name).items(num_tweets)
    ]

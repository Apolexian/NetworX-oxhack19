import tweepy as tw
import json
import logging


def auth():
    with open('creds.json') as creds:
        credentials = json.load(creds)

    authi = tw.auth.OAuthHandler(credentials["consumer_key"], credentials["consumer_secret"])
    authi.set_access_token(credentials["access_token"], credentials["access_secret"])
    api = tw.API(authi, wait_on_rate_limit=True)
    return api


def geo_get_users(api, n, geocode="40.68908,-73.95860,200km", lang="en", date_since="2018-10-15"):
    users_names = set()
    while len(users_names) <= n:
        for tweet in tw.Cursor(
                api.search,
                geocode=geocode,
                lang=lang,
                since=date_since).items(10):
            users_names.add(tweet.user.screen_name)
    return list(users_names)

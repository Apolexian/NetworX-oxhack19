import json

import tweepy as tw


def auth():
    with open('creds.json') as creds:
        credentials = json.load(creds)

    authi = tw.auth.OAuthHandler(credentials["consumer_key"], credentials["consumer_secret"])
    authi.set_access_token(credentials["access_token"], credentials["access_secret"])
    api = tw.API(authi, wait_on_rate_limit=True)
    return api


import tweepy as tw
import json

with open('creds.json') as creds:
    credentials = json.load(creds)

auth = tw.auth.OAuthHandler(credentials["consumer_key"], credentials["consumer_secret"])
auth.set_access_token(credentials["access_token"], credentials["access_secret"])

api = tw.API(auth, wait_on_rate_limit=True)
date_since = "2018-10-15"
users_names = set()
for tweet in tw.Cursor(api.search,
                       geocode="40.68908,-73.95860,200km",
                       lang="en",
                       since=date_since).items(100):
    users_names.add(tweet.user.screen_name)
    print("got user: " + str(tweet.user.screen_name))

user_tweets = {}
for user in users_names:
    for tweet in tw.Cursor(api.user_timeline, screen_name=user).items(100):
        print("extracting tweet for: " + str(user))
        if user in user_tweets.keys():
            user_tweets[user].append((tweet.text, tweet.entities))
        else:
            user_tweets[user] = [(tweet.text, tweet.entities)]

with open('user_tweets.json', 'a') as f:
    print("dumped")
    json.dump(user_tweets, f, ensure_ascii=False, indent=4)


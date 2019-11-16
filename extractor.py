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
                       since=date_since).items(300):
    print(tweet)
    users_names.add(tweet.user.screen_name)

user_friends = {}
user_tweets = {}
for user in users_names:
    print(user)
    for tweet in tw.Cursor(api.user_timeline, screen_name=user).items(100):
        if user in user_tweets.keys():
            user_tweets[user].append(tweet.text)
        else:
            user_tweets[user] = [tweet.text]

with open('user_tweets.json', 'w') as f:
    print("dumped")
    json.dump(user_tweets, f, ensure_ascii=False, indent=4)

for user in users_names:
    for friend in tw.Cursor(api.friends, screen_name=user).items(100):
        if user in user_friends.keys():
            user_friends[user].append(friend.screen_name)
        else:
            user_friends[user] = [friend.screen_name]

with open('user_friends.json', 'w') as f:
    print("dumped friends")
    json.dump(user_friends, f, ensure_ascii=False, indent=4)

from tweepy import Cursor
from collections import Counter
import logging


def scrape_user(api, starting_account, bf_lim=10, tweet_lim=100):
    user_friends = get_mentions(api, starting_account, tweet_lim)

    mentions_dict = {starting_account: list(set(user_friends))}
    logging.info(f"mentions_dict={mentions_dict}")

    mentions_counter = Counter(user_friends)
    top_ten_friends = mentions_counter.most_common(bf_lim)
    logging.info(f"top_ten_friends={top_ten_friends}")
    for user_name, _ in top_ten_friends:
        account_mentions = get_mentions(api, user_name, tweet_lim)
        mentions_dict[user_name] = list(set(account_mentions))

    return mentions_dict


def get_mentions(api, user_name, tweet_lim):
    user_friends = []
    for tweet in Cursor(api.user_timeline, id=user_name).items(tweet_lim):
        # if "user_mentions" in status.entities.keys():
        user_friends.extend([user["screen_name"] for user in tweet.entities["user_mentions"]])
    return user_friends


if __name__ == "__main__":
    from extractor import auth
    import json

    api = auth()
    mentions = scrape_user("kamilgorzynski", tweet_lim=100, bf_lim=10)
    with open("mentions.json", "w") as f:
        json.dump(mentions, f, ensure_ascii=False, indent=4)

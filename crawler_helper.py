from tweepy import Cursor, TweepError
import pandas as pd
import time

### put api here

api = None


def get_mentions_of_user(starting_account):
    db = {starting_account : None}
    accounts_to_crawl = [starting_account]
    acc_counter = 0
    for account in accounts_to_crawl:
        print(f"{acc_counter}: {account}")
        account_mentions = []
        acc_counter += 1
        if acc_counter > 100:
            break
        try:
            for status in Cursor(api.user_timeline, id=account).items(100):
                if "user_mentions" in status.entities:
                    for mention in status.entities["user_mentions"]:
                        account_mentions.append(mention["screen_name"])
            print(len(account_mentions))
            account_mentions = pd.Series(account_mentions).value_counts()
            print(account_mentions)
            account_mentions = list(account_mentions.index)
            db[account] = account_mentions
            accounts_to_crawl.extend(account_mentions[:10])
        except TweepError:
            time.sleep(5)
            print('boom')
            continue
    for k in db:
        print(f"{k}: {db[k]}")
    print(pd.Series(data=accounts_to_crawl).value_counts())
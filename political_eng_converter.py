import string
from tweepy import Cursor, TweepError

TWEET_LIMIT = 100


def get_political_terms():
    f = open('political_terms.txt', 'r')
    terms = f.read().split("\n")
    f.close()
    return terms


def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))



def extract_account_engagement(accounts, api):

    political_terms = get_political_terms()

    engagement_output = {}

    for account in accounts:

        terms_count = 0

        try:

            for status in Cursor(api.user_timeline, id=account).items(TWEET_LIMIT):

                table = str.maketrans(dict.fromkeys(string.punctuation))

                content = status.text.translate(table).split()

                common_terms = intersection(political_terms, content)

                terms_count += len(common_terms)

            engagement_output[account] = terms_count/TWEET_LIMIT

        except TweepError:

            continue

    return engagement_output



import string

TWEET_LIMIT = 100


def get_political_terms():
    f = open('political_terms.txt', 'r')
    terms = f.read().split("\n")
    f.close()
    return terms


def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))


def assign_political_engagement(dictionary):
    political_terms = get_political_terms()
    political_engagement = {}
    for user, tweets in dictionary.items():
        terms_count = 0
        tweet_count = 0
        for tweet in tweets:
            table = str.maketrans(dict.fromkeys(string.punctuation))
            content = tweet.translate(table).split()
            common_terms = intersection(political_terms, content)
            tweet_count += 1
            terms_count += len(common_terms)
        if tweet_count != 0:
            political_engagement[user] = terms_count / tweet_count
        else:
            political_engagement[user] = 0
    return political_engagement

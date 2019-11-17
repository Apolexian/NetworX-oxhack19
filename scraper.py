# import pandas as pd
from tweepy import Cursor
from tweepy.error import TweepError
import extractor
from crawler_helper import scrape_user
import json
import logging
import traceback

logging.basicConfig(
    format="%(asctime)s.%(msecs)03d - %(module)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
    level=logging.INFO,
)

api = extractor.auth()

logging.warning(f"Geoget users")
user_names = extractor.geo_get_users(api, 100)
logging.warning(f"... user_names={user_names} ({len(user_names)})")
for user in user_names:
    logging.warning(f"Scraping user {user}")
    try:
        mentions_dict = scrape_user(api, user)
        with open(f"scrape/scraped-{user}.json", "a") as f:
            json.dump(mentions_dict, f, ensure_ascii=False, indent=4)
    except TweepError:
        traceback.print_exc()
        pass


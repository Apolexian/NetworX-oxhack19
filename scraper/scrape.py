import json
import logging
import traceback
import uuid

from tweepy import Cursor
from tweepy.error import TweepError

from .auth import auth
from .crawler_helper import scrape_user, geo_get_users
from .graph_creation import add_friend, add_user, driver

logging.basicConfig(
    format="%(asctime)s.%(msecs)03d - %(module)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
    level=logging.INFO,
)

api = auth()

logging.warning(f"Geoget users")
user_names = geo_get_users(api, 100)
logging.warning(f"... user_names={user_names} ({len(user_names)})")
for user in user_names:
    logging.warning(f"Scraping user {user}")
    try:
        mentions_dict = scrape_user(api, user)
        # add to neo4j
        with driver.session() as s:
            for name, friend_list in mentions_dict:
                s.write_transaction(add_user, name, friend_list)
                s.write_transaction(add_friend, name, mentions_dict.keys())
    except TweepError:
        traceback.print_exc()
        pass

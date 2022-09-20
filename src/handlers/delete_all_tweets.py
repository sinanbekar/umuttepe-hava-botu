import logging
import os
import sys

import azure.functions as func  # type: ignore


sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src"))
)

from umuttepe_hava_botu import TwitterActions


twitter = None


def main(timer: func.TimerRequest) -> None:
    logging.info("Deleting all expired tweets...")

    global twitter
    if twitter is None:
        twitter = TwitterActions.connect()
        logging.info("Connected to the Twitter API.")

    twitter.delete_expired_tweets()
    logging.info("All expired tweets deleted.")

import sys
import os
import logging

import azure.functions as func

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))

from umuttepe_hava_botu import Twitter

twitter = None

def main(timer: func.TimerRequest) -> None:
    logging.info('Deleting all expired tweets...')
    
    global twitter
    if twitter is None:
        twitter = Twitter()
        twitter.connect()
        logging.info("Connected to the Twitter API.")

    twitter.delete_expired_tweets()
    logging.info("All expired tweets deleted.");




    
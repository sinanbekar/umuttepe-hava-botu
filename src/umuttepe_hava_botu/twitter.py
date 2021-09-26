from .live_stream_data import LiveStreamPhotoGenerator
from .weather_data import WeatherComParser

import tweepy
import time
from datetime import timezone
import os


class Twitter:

    def __init__(self) -> None:
        pass

    def connect(self) -> None:
        self.auth = tweepy.OAuthHandler(
            os.getenv('TWITTER_CONSUMER_KEY'),
            os.getenv('TWITTER_CONSUMER_SECRET')
        )
        self.auth.set_access_token(
            os.getenv('TWITTER_ACCESS_TOKEN'),
            os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
        )
        self.api = tweepy.API(self.auth)

    def publish_weather_tweet(self) -> None:

        tweets = self.api.user_timeline(
            screen_name=self.api.auth.get_username(), count=5)

        publish_tweet = True

        for tweet in tweets:
            # TODO: better approach
            if "Umuttepe'de hava şu an" in tweet.text and \
                    (time.time() - tweet.created_at.replace(tzinfo=timezone.utc).timestamp()) / 60 < 20:
                publish_tweet = False

        if publish_tweet:
            photos = LiveStreamPhotoGenerator().get_photos()
            weather_text = WeatherComParser().get_weather_text()
            media_ids = []

            for filename in photos:
                res = self.api.media_upload(filename)
                media_ids.append(res.media_id)

            self.api.update_status(status=weather_text, media_ids=media_ids)

    def delete_expired_tweets(self):
        tweets = self.api.user_timeline(
            screen_name=self.api.auth.get_username())
        for tweet in tweets:
           # TODO: better approach
            if "Umuttepe'de hava şu an" in tweet.text and \
                    (time.time() - tweet.created_at.replace(tzinfo=timezone.utc).timestamp()) / 3600 > 24:
                self.api.destroy_status(tweet.id)

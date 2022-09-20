from __future__ import annotations
import logging
from typing import Any
import tweepy  # type: ignore
import time
from datetime import timezone
from .util import get_env_var
from .live_stream import get_frames
from .weather_data import get_weather_data


class TwitterActions:
    WEATHER_STARTING_PHRASE = "Umuttepe'de hava şu an"

    def __init__(self, api: tweepy.API) -> None:
        self.api = api

    @classmethod
    def connect(cls) -> TwitterActions:
        auth = tweepy.OAuth1UserHandler(
            get_env_var("TWITTER_CONSUMER_KEY"),
            get_env_var("TWITTER_CONSUMER_SECRET"),
            get_env_var("TWITTER_ACCESS_TOKEN"),
            get_env_var("TWITTER_ACCESS_TOKEN_SECRET"),
        )

        twitter = cls(tweepy.API(auth))

        return twitter

    def publish_tweet(self, text: str, frames: list[Any] = []) -> None:
        media_ids = []

        try:
            if frames:
                for filename in frames:
                    res = self.api.media_upload(filename)
                    media_ids.append(res.media_id)
        except Exception:
            logging.exception(
                f"An error occurred while uploading media to the Twitter."
            )

        self.api.update_status(status=text, media_ids=media_ids)

    def is_tweet_expired(self, tweet: tweepy.Status, sec: int) -> bool:
        # just in case running multiple times accidentally
        return bool(
            time.time() - tweet.created_at.replace(tzinfo=timezone.utc).timestamp()
            > sec
        )

    def publish_weather_tweet(self) -> None:
        publish_tweet = True
        tweets = self.api.user_timeline(
            screen_name=self.api.auth.get_username(), count=5
        )

        for tweet in tweets:
            if (
                self.WEATHER_STARTING_PHRASE in tweet.text
                and not self.is_tweet_expired(tweet, 60 * 20)
            ):  # 20 mins
                publish_tweet = False

        if publish_tweet:
            weather_data = get_weather_data()

            frames = []
            try:
                frames = get_frames()
            except:
                logging.warning("Live camera feed offline, tweeting without frames.")

            self.publish_tweet(weather_data, frames)

    def delete_expired_tweets(self) -> None:
        tweets = self.api.user_timeline(
            screen_name=self.api.auth.get_username(), count=50
        )
        for tweet in tweets:
            if self.WEATHER_STARTING_PHRASE in tweet.text and self.is_tweet_expired(
                tweet, 24 * 3600
            ):  # 24 hours
                self.api.destroy_status(tweet.id)

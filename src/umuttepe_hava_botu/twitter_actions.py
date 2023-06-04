from __future__ import annotations
import logging
import os
import redis # type: ignore
from typing import Any
import tweepy  # type: ignore
import datetime
from .util import get_env_var
from .live_stream import get_frames
from .weather_data import get_weather_data

published_tweets_key = "published_tweets"

class TwitterActions:
    WEATHER_STARTING_PHRASE = "Umuttepe'de hava şu an"

    def __init__(self, api: tweepy.API, client: tweepy.Client, r: redis.StrictRedis) -> None:
        self.api = api
        self.client = client
        self.r = r

    @classmethod
    def connect(cls) -> TwitterActions:
        consumer_key = get_env_var("TWITTER_CONSUMER_KEY")
        consumer_secret = get_env_var("TWITTER_CONSUMER_SECRET")
        access_token = get_env_var("TWITTER_ACCESS_TOKEN")
        access_token_secret = get_env_var("TWITTER_ACCESS_TOKEN_SECRET")

        # v2
        client = tweepy.Client(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token=access_token,
            access_token_secret=access_token_secret,
        )

        # v1.1
        # We need this authentication also because to add media it only works with api v1.1
        auth = tweepy.OAuth1UserHandler(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token=access_token,
            access_token_secret=access_token_secret,
        )
        api = tweepy.API(auth)

        r = redis.StrictRedis(
            host=get_env_var("REDIS_HOST"),
            port=get_env_var("REDIS_PORT"),
            password=get_env_var("REDIS_PASSWORD"),
            charset="utf-8",
            decode_responses=True,
        )

        bot = cls(api, client, r)

        return bot

    def publish_tweet(self, text: str, frames: list[Any] = []) -> None:
        media_ids = []

        try:
            if frames:
                for filename in frames:
                    res = self.api.media_upload(filename)
                    media_ids.append(res.media_id)
                    os.unlink(filename)
        except Exception:
            logging.exception(
                f"An error occurred while uploading media to the Twitter."
            )

        ct = datetime.datetime.now()
        ts = int(ct.timestamp())
        tweet = self.client.create_tweet(text=text, media_ids=media_ids)
        tweet_id = tweet.data["id"]
        self.r.zadd(published_tweets_key, {tweet_id: ts})

    def publish_weather_tweet(self) -> None:
        weather_data = get_weather_data()

        frames = []
        try:
            frames = get_frames()
        except:
            logging.warning("Live camera feed offline, tweeting without frames.")

        self.publish_tweet(weather_data, frames)

    def delete_expired_tweets(self) -> None:
        ct = datetime.datetime.now()
        ts = int(ct.timestamp())
        before_24h = ts - 24 * 3600
        
        tweet_ids = self.r.zrangebyscore(published_tweets_key, min=before_24h, max=ts)
        for tweet_id in tweet_ids:
            try:
                self.client.delete_tweet(tweet_id)
            except:
                pass

        self.r.zrem(published_tweets_key, *tweet_ids)

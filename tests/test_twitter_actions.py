from __future__ import annotations
import os
from pytest_mock import MockerFixture  # type: ignore
import tweepy  # type: ignore
from umuttepe_hava_botu import TwitterActions


def test_twitter_connect(mocker: MockerFixture) -> None:
    mock_oauth_handler = mocker.patch("tweepy.OAuth1UserHandler", autospec=True)
    mock_api = mocker.patch("tweepy.API", autospec=True)
    twitter_api_env = {
        "TWITTER_CONSUMER_KEY": "consumer_key",
        "TWITTER_CONSUMER_SECRET": "consumer_secret",
        "TWITTER_ACCESS_TOKEN": "access_token",
        "TWITTER_ACCESS_TOKEN_SECRET": "access_token_secret",
    }
    mocker.patch.dict(os.environ, twitter_api_env)

    twitter = TwitterActions.connect()

    assert isinstance(twitter, TwitterActions)
    assert isinstance(twitter.api, tweepy.API.__class__)
    assert twitter.api == mock_api.return_value
    mock_oauth_handler.assert_called_once_with(*list(twitter_api_env.values()))
    mock_api.assert_called_once_with(mock_oauth_handler.return_value)


def test_publish_tweet_success(mocker: MockerFixture) -> None:
    status_text = "Weather"
    media_ids = [1263145271946551300, 1263145271946551301]
    mock_twitter_api = mocker.patch("tweepy.API", autospec=True)
    mock_twitter_api.update_status = mocker.MagicMock()
    mock_twitter_api.media_upload = mocker.MagicMock()
    type(mock_twitter_api.media_upload.return_value).media_id = mocker.PropertyMock(
        side_effect=media_ids
    )
    mocker.patch("os.unlink")

    twitter = TwitterActions(mock_twitter_api)
    twitter.publish_tweet(status_text, ["/tmp/frame123456", "/tmp/frame234567"])

    mock_twitter_api.update_status.assert_called_once_with(
        status=status_text, media_ids=media_ids
    )


def test_publish_tweet_failure(mocker: MockerFixture) -> None:
    status_text = "Weather"
    media_ids = [1263145271946551300, 1263145271946551301]
    mock_twitter_api = mocker.patch("tweepy.API", autospec=True)
    mock_twitter_api.update_status = mocker.MagicMock()
    mock_twitter_api.media_upload = mocker.MagicMock(
        side_effect=tweepy.TweepyException()
    )
    type(mock_twitter_api.media_upload.return_value).media_id = mocker.PropertyMock(
        side_effect=media_ids
    )
    mocker.patch("os.unlink")

    twitter = TwitterActions(mock_twitter_api)
    twitter.publish_tweet(status_text, ["/tmp/frame123456", "/tmp/frame234567"])

    mock_twitter_api.update_status.assert_called_once_with(
        status=status_text, media_ids=[]
    )

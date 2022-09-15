from dotenv import load_dotenv
from celery import Celery
from . import celeryconfig
from .helpers import get_cache_dir
from .twitter import Twitter

APP_NAME = 'umuttepe_hava_botu'

app = Celery(APP_NAME)
app.config_from_object(celeryconfig)

twitter = Twitter()

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs) -> None:
    twitter.connect()
    publish_weather_tweet.delay()  # Run when first start
    delete_expired_tweets.delay()
    sender.add_periodic_task(
        30 * 60.0,
        publish_weather_tweet.s(),
        name='publish weather tweet every 30 min'
    )
    sender.add_periodic_task(
        3 * 60.0 * 60,
        delete_expired_tweets.s(), name="delete expired tweets"
    )

@app.task
def publish_weather_tweet() -> None:
    twitter.publish_weather_tweet()


@app.task
def delete_expired_tweets() -> None:
    twitter.delete_expired_tweets()

def run():
    load_dotenv()
    print("Starting: ", APP_NAME)

    # Run Celery
    app.worker_main(argv=['-A', APP_NAME, 'worker', '-B',
                          '-s',  get_cache_dir() + '/celerybeat-schedule', '--concurrency=5',  '--loglevel=info'])


if __name__ == '__main__':
    run()

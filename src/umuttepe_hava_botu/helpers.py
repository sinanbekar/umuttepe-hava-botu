import os
import tempfile
from urllib.parse import urlparse

def get_cache_dir() -> str:
    cache_dir = tempfile.gettempdir()
    return cache_dir

def get_broker_url() -> str:
    broker_url = os.getenv('CELERY_BROKER_URL', 'filesystem://')
    return broker_url

def get_broker_dir() -> str:
    broker_dir = os.getenv('CELERY_BROKER_FOLDER', get_cache_dir() + '/broker')

    for f in ['out', 'processed']:
        if not os.path.exists(os.path.join(broker_dir, f)):
            os.makedirs(os.path.join(broker_dir, f))

    return broker_dir

    
def uri_validator(x):
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc])
    except:
        return False

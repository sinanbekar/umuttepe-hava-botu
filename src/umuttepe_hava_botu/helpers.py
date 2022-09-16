import tempfile
from urllib.parse import urlparse

def get_cache_dir() -> str:
    cache_dir = tempfile.gettempdir()
    return cache_dir
    
def uri_validator(x):
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc])
    except:
        return False

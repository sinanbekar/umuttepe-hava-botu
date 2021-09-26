from umuttepe_hava_botu.live_stream_data import LiveStreamUrlParser, LiveStreamPhotoGenerator
from umuttepe_hava_botu.helpers import uri_validator
import os


def test_m3u8_stream_url():
    assert uri_validator(LiveStreamUrlParser().get_m3u8_stream_url()) == True

def test_m3u8_stream_downlod():
    generator = LiveStreamPhotoGenerator()
    generator.download_m3u8_video(LiveStreamUrlParser().get_m3u8_stream_url())
    isSuccess = os.path.isfile(generator.video_dir) == True and os.path.getsize(
        generator.video_dir) > 100
    os.remove(generator.video_dir)
    assert isSuccess == True

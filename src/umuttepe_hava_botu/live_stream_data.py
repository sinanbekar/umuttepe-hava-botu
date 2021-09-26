from typing import List, Final
import m3u8
import cv2
import numpy as np

import requests
import os

from .helpers import get_cache_dir

MEDIATRIPLE_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0",
    "referer": "http://playercache.mediatriple.net/",
}


class LiveStreamUrlParser:

    MEDIATRIPLE_UMUTTEPE_STREAM_URL_DATA: Final[str] = "https://titan.mediatriple.net/?br=broadcast_606c2b124aa9c"

    def get_m3u8_stream_url(self) -> str:
        r = requests.get(self.MEDIATRIPLE_UMUTTEPE_STREAM_URL_DATA,
                         headers=MEDIATRIPLE_HEADERS)
        return r.json()['streams'][0]['url']


class LiveStreamPhotoGenerator:

    def __init__(self) -> None:
        self.save_name = "video.mp4"
        self.video_dir = get_cache_dir() + '/' + self.save_name
        self.image_dir = get_cache_dir() + '/frames'

        if not os.path.exists(self.image_dir):
            os.makedirs(self.image_dir)

    def get_real_url(self, url, headers) -> str:
        playlist = m3u8.load(uri=url, headers=headers)
        return playlist.playlists[0].absolute_uri

    def download_m3u8_video(self, url) -> None:
        playlist = m3u8.load(self.get_real_url(
            url, headers=MEDIATRIPLE_HEADERS), headers=MEDIATRIPLE_HEADERS)
        for i, seg in enumerate(playlist.segments, 1):
            r = requests.get(seg.absolute_uri, headers=MEDIATRIPLE_HEADERS)
            data = r.content
            with open(self.video_dir, "ab" if i != 1 else "wb") as f:
                f.write(data)

    def get_photos(self) -> List[str]:

        self.download_m3u8_video(
            LiveStreamUrlParser().get_m3u8_stream_url())

        if os.path.getsize(self.video_dir) < 100:
            # Fail, try again
            # TODO Better approach
            self.download_m3u8_video(
                LiveStreamUrlParser().get_m3u8_stream_url())

        cap = cv2.VideoCapture(self.video_dir)

        # Randomly select 30 frames
        frameIds = cap.get(cv2.CAP_PROP_FRAME_COUNT) * \
            np.random.uniform(size=30)
        cap.set(cv2.CAP_PROP_POS_FRAMES, np.amax(frameIds))
        ret, frame1 = cap.read()
        cap.set(cv2.CAP_PROP_POS_FRAMES, np.amin(frameIds))
        ret, frame2 = cap.read()
        cv2.imwrite(self.image_dir + '/frame1.jpg', frame1)
        cv2.imwrite(self.image_dir + '/frame2.jpg', frame2)

        os.remove(self.video_dir)

        return [self.image_dir + '/frame1.jpg', self.image_dir + '/frame2.jpg']

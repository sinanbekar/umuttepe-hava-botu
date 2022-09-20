from __future__ import annotations
import io
from typing import Optional
import m3u8  # type: ignore
from m3u8 import Segment, M3U8
import cv2  # type: ignore


class LiveStreamFrameGenerator:
    # TODO: set when deploy
    # https://umuttepe-hava.vercel.app/api/kocaeliyiseyret

    STREAM_ID = "c8h3fufmm25qqqh92540"
    STREAM_CONTENT_TEMPLATE = "https://content.tvkur.com/l/{stream_id}/master.m3u8"

    def __init__(self) -> None:
        self._stream: Optional[M3U8] = None
        self._segments: Optional[list[Segment]] = None

    def get_stream(self) -> M3U8:
        if self._stream is None:
            self._stream = m3u8.load(
                self.STREAM_CONTENT_TEMPLATE.format(stream_id=self.STREAM_ID)
            )

        return self._stream

    def _get_first_and_last_segment(self) -> list[Segment]:
        if self._segments is None:
            stream = self.get_stream()
            self._segments = [
                stream.segments[0],
                stream.segments[-1],
            ]  # first and last segment

        return self._segments

    def _get_first_frame(self, video_url: str) -> bytes:
        cap = cv2.VideoCapture(video_url)
        _, frame = cap.read()
        img_encode = cv2.imencode(".jpg", frame)[1]
        img_bytes: bytes = img_encode.tobytes()

        return img_bytes

    def get_segment_first_frame(self, segment: Segment) -> bytes:
        return self._get_first_frame(segment.absolute_uri)

    def generate_frames(self) -> list[io.BytesIO]:
        file_like_frames = []

        for segment in self._get_first_and_last_segment():
            frame_bytes = self.get_segment_first_frame(segment)
            file_like_frames.append(io.BytesIO(frame_bytes))

        return file_like_frames


def get_frames() -> list[io.BytesIO]:
    return LiveStreamFrameGenerator().generate_frames()

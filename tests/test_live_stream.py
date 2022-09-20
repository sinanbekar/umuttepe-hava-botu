from __future__ import annotations
from pytest_mock import MockerFixture  # type: ignore
from m3u8 import M3U8  # type: ignore
from umuttepe_hava_botu.live_stream import LiveStreamFrameGenerator
from segment import create_segment


def test_get_stream(mocker: MockerFixture) -> None:
    mock_m3u8_load = mocker.patch("m3u8.load", return_value=M3U8())

    live_stream = LiveStreamFrameGenerator()
    stream = live_stream.get_stream()

    assert isinstance(stream, M3U8)
    mock_m3u8_load.assert_called_once_with(
        live_stream.STREAM_CONTENT_TEMPLATE.format(stream_id=live_stream.STREAM_ID)
    )


def test_get_segment_first_frame(mocker: MockerFixture) -> None:
    mock_get_first_frame = mocker.patch.object(
        LiveStreamFrameGenerator,
        "_get_first_frame",
        return_value="dummy_frame".encode(),
    )
    mock_segment = create_segment()

    live_stream = LiveStreamFrameGenerator()
    frame = live_stream.get_segment_first_frame(mock_segment)

    assert type(frame) == bytes
    mock_get_first_frame.assert_called_once_with(mock_segment.absolute_uri)


def test_generate_frames(mocker: MockerFixture) -> None:
    [first_s, last_s] = [create_segment() for _ in range(2)]
    mocker.patch.object(
        LiveStreamFrameGenerator,
        "_get_first_and_last_segment",
        return_value=[first_s, last_s],
    )

    mock_frames_as_bytes = ["frame1".encode(), "frame2".encode()]
    mock_get_segment_first_frame_as_bytes = mocker.patch.object(
        LiveStreamFrameGenerator,
        "get_segment_first_frame",
        side_effect=mock_frames_as_bytes,
    )
    live_stream = LiveStreamFrameGenerator()
    frames = live_stream.generate_frames()

    assert [frame.read() for frame in frames] == mock_frames_as_bytes
    assert mock_get_segment_first_frame_as_bytes.call_count == 2

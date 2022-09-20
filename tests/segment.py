from unittest.mock import NonCallableMock
from m3u8 import Segment  # type: ignore
import random


def create_segment() -> NonCallableMock:
    segment = NonCallableMock(spec=Segment)
    segment.absolute_uri = f"http://media.example.com/segment-{random.randint(1, 9)}.ts"
    return segment

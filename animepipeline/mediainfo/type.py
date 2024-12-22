from datetime import datetime
from typing import List, Tuple

from pydantic import BaseModel, FilePath


class FileNameInfo(BaseModel):
    path: FilePath
    episode: int
    name: str
    uploader: str
    type: str = "WEBRip"


class MediaInfo(BaseModel):
    release_name: str
    release_date: datetime
    release_size: str  # 1.35 GiB
    release_format: str  # Matroska
    overall_bitrate: str  # 1919.8 Mb/s
    resolution: Tuple[int, int]  # (1920, 1080)
    bit_depth: int  # 10
    frame_rate: float  # 23.976
    format: str  # HEVC
    format_profile: str  # Main@L5@Main
    audios: List[Tuple[str, int, str]]  # Chinese, 2 channels, FLAC
    subtitles: List[Tuple[str, str]]  # CHS, PGS

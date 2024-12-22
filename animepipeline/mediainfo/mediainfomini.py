import json
from datetime import datetime
from pathlib import Path
from typing import List, Tuple, Union

import pymediainfo
from loguru import logger

from animepipeline.mediainfo.type import FileNameInfo, MediaInfo


def get_media_info(video_path: Union[str, Path]) -> MediaInfo:
    """
    Get the mini media info of the video file

    :param video_path:
    """
    logger.info(f"Get media info of {video_path}...")

    video_path = Path(video_path)

    encode_media_info = pymediainfo.MediaInfo.parse(video_path, output="JSON")
    encode_tracks = json.loads(encode_media_info)["media"]["track"]

    release_name = video_path.name
    release_date = datetime.now()
    # date_YMd = release_date.strftime("%Y:%M:%d")

    try:
        release_size = encode_tracks[0]["FileSize_String"]
    except Exception:
        logger.warning(f'Failed to get "FileSize_String" of {video_path}')
        release_size = encode_tracks[0]["FileSize"]
        release_size = round(int(release_size) / (1024 * 1024), 2)
        if release_size > 1000:
            release_size = round(release_size / 1024, 2)
            release_size = str(release_size) + " GiB"
        else:
            release_size = str(release_size) + " MiB"

    try:
        release_format = encode_tracks[0]["Format"]
    except Exception as e:
        logger.warning(f'Failed to get "Format" of {video_path}, set to "Unknown", {e}')
        release_format = "Unknown"

    try:
        overall_bitrate = encode_tracks[0]["OverallBitRate_String"]
    except Exception:
        logger.warning(f'Failed to get "OverallBitRate_String" of {video_path}')
        try:
            overall_bitrate = encode_tracks[0]["OverallBitRate"]
            overall_bitrate = round(int(overall_bitrate) / 1000, 2)
            if overall_bitrate > 10000:
                overall_bitrate = round(overall_bitrate / 1000, 2)
                if overall_bitrate > 1000:
                    overall_bitrate = round(overall_bitrate / 1000, 2)
                    overall_bitrate = str(overall_bitrate) + " Gb/s"
                else:
                    overall_bitrate = str(overall_bitrate) + " Mb/s"
            else:
                overall_bitrate = str(overall_bitrate) + " kb/s"
        except Exception as e:
            logger.warning(f'Failed to get "OverallBitRate" of {video_path}, set to "Unknown", {e}')
            overall_bitrate = "Unknown"

    # VIDEO TRACK
    resolution = (0, 0)
    bit_depth = 0
    frame_rate = 0.0
    video_format = "Unknown"
    format_profile = "Unknown"

    video_track_id = 0
    try:
        for _, video_track in enumerate(encode_tracks):
            if video_track["@type"] == "Video":
                resolution = (int(video_track["Width"]), int(video_track["Height"]))
                bit_depth = int(video_track["BitDepth"])
                frame_rate = float(video_track["FrameRate"])
                video_format = video_track["Format"]
                format_profile = video_track["Format_Profile"]
                video_track_id += 1
    except Exception as e:
        logger.warning(f"Exceptional video track: {video_track_id} of {video_path}, {e}")

    if video_track_id != 1:
        logger.warning(f"There may be multiple video tracks or no video tracks, please check {video_path}")

    # AUDIO TRACK
    audios: List[Tuple[str, int, str]] = []

    audio_track_id = 1
    try:
        for _, audio_track in enumerate(encode_tracks):
            if audio_track["@type"] == "Audio":
                language = audio_track.get("Language_String", audio_track.get("Language", "Ambiguous!!!"))
                audios.append((language, int(audio_track["Channels"]), audio_track["Format"]))
                audio_track_id += 1
    except Exception as e:
        logger.warning(f"Exceptional audio track: {audio_track_id} of {video_path}, {e}")

    # SUBTITLE TRACK
    subtitles: List[Tuple[str, str]] = []

    subtitle_track_id = 1
    try:
        for _, subtitle_track in enumerate(encode_tracks):
            if subtitle_track["@type"] == "Text":
                language = subtitle_track.get("Language_String", subtitle_track.get("Language", "Ambiguous!!!"))
                subtitles.append((language, subtitle_track["Format"]))
                subtitle_track_id += 1
    except Exception as e:
        logger.warning(f"Exceptional subtitle track: {subtitle_track_id} of {video_path}, {e}")

    return MediaInfo(
        release_name=release_name,
        release_date=release_date,
        release_size=release_size,
        release_format=release_format,
        overall_bitrate=overall_bitrate,
        resolution=resolution,
        bit_depth=bit_depth,
        frame_rate=frame_rate,
        format=video_format,
        format_profile=format_profile,
        audios=audios,
        subtitles=subtitles,
    )


def gen_file_name(anime_info: FileNameInfo) -> str:
    """
    Auto generate the file name, based on the media info of the file

    anime_info: FileNameInfo (path: xx.mkv, episode: 1, name: Fate/Kaleid Liner Prisma Illya, uploader: TensoRaws, type: WEBRip)

    -> [TensoRaws] Fate/Kaleid Liner Prisma Illya [01] [WEBRip 1080p HEVC-10bit FLAC].mkv

    :param anime_info: FileNameInfo
    :return:
    """
    media_info = get_media_info(anime_info.path)
    resolution_heigh = str(media_info.resolution[1]) + "p"
    bit_depth = str(media_info.bit_depth) + "bit"

    video_format = media_info.format

    audio_format_list = [audio[2] for audio in media_info.audios]
    audio_format = "FLAC" if "FLAC" in audio_format_list else audio_format_list[0]

    file_format = Path(anime_info.path).suffix

    return f"[{anime_info.uploader}] {anime_info.name} [{str(anime_info.episode).zfill(2)}] [{anime_info.type} {resolution_heigh} {video_format}-{bit_depth} {audio_format}]{file_format}"


def rename_file(anime_info: FileNameInfo) -> Path:
    """
    Rename the file name, based on the media info of the file

    :param anime_info: FileNameInfo
    :return:
    """
    anime_path = Path(anime_info.path)

    gen_name = gen_file_name(anime_info)
    gen_path = anime_path.parent / gen_name

    if gen_path.exists():
        gen_path.unlink()
        logger.warning(f"Encode File already exists, remove it: {gen_path}")

    anime_path.rename(gen_path)

    return gen_path

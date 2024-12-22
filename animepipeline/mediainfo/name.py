from pathlib import Path

from loguru import logger

from animepipeline.mediainfo.mediainfo import get_media_info
from animepipeline.mediainfo.type import FileNameInfo


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

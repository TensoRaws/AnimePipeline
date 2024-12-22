from pathlib import Path
from typing import List, Union

from animepipeline.mediainfo import get_media_info


def gen_media_info_block(video_path: Union[str, Path], uploader: str = "TensoRaws") -> str:
    """
    Generate a code block for media info.

    RELEASE.NAME........: [TensoRaws] Fate/Kaleid Liner Prisma Illya [01] [WEBRip 2160p HEVC-10bit FLAC].mkv
    RELEASE.DATE........: 2022-07-09
    RELEASE.SIZE........: 114514.1 GiB
    RELEASE.FORMAT......: Matroska
    OVERALL.BITRATE.....: 1919.8 Mb/s
    RESOLUTION..........: 3840x2160
    BIT.DEPTH...........: 10 bits
    FRAME.RATE..........: 60.000 FPS
    VIDEO...............: HEVC, Main@L5@Main
    AUDIO#01............: Chinese, 8 channels, E-AC-3
    AUDIO#02............: Engilsh, 2 channels, AAC
    SUBTITLE#01.........: CHS, PGS
    SUBTITLE#02.........: CHT, ASS
    SUBTITLE#03.........: CHT, SRT
    SUBTITLE#04.........: CHT&ENG, ASS
    SUBTITLE#05.........: ENG&CHT, ASS
    UPLOADER............: TensoRaws
    """
    media_info = get_media_info(video_path=video_path)

    write_info_list: List[str] = []

    write_info_list.append("RELEASE.NAME........: " + media_info.release_name)
    write_info_list.append("RELEASE.DATE........: " + media_info.release_date.strftime("%Y-%m-%d"))
    write_info_list.append("RELEASE.SIZE........: " + media_info.release_size)
    write_info_list.append("RELEASE.FORMAT......: " + media_info.release_format)
    write_info_list.append("OVERALL.BITRATE.....: " + media_info.overall_bitrate)
    # VIDEO TRACK
    write_info_list.append(
        "RESOLUTION..........: " + str(media_info.resolution[0]) + "x" + str(media_info.resolution[1])
    )
    write_info_list.append("BIT.DEPTH...........: " + str(media_info.bit_depth) + " bits")
    write_info_list.append("FRAME.RATE..........: " + str(media_info.frame_rate) + " FPS")
    write_info_list.append("VIDEO...............: " + media_info.format + ", " + media_info.format_profile)
    # AUDIO TRACK
    for audio_track_id, audio_track in enumerate(media_info.audios):
        write_info_list.append(
            "AUDIO#"
            + str(audio_track_id).zfill(2)
            + "............: "
            + audio_track[0]
            + ", "
            + str(audio_track[1])
            + " channels, "
            + audio_track[2]
        )
    # SUBTITLE TRACK
    for subtitle_track_id, subtitle_track in enumerate(media_info.subtitles):
        write_info_list.append(
            "SUBTITLE#" + str(subtitle_track_id).zfill(2) + ".........: " + subtitle_track[0] + ", " + subtitle_track[1]
        )
    write_info_list.append("UPLOADER............: " + uploader)

    return "\n".join(write_info_list)

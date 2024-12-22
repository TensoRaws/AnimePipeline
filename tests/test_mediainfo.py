from animepipeline.mediainfo import gen_file_name, get_media_info
from animepipeline.mediainfo.type import FileNameInfo

from .util import TEST_VIDEO_PATH


def test_get_media_info() -> None:
    media_info = get_media_info(video_path=TEST_VIDEO_PATH)
    print(media_info)


def test_gen_file_name() -> None:
    anime_info = FileNameInfo(
        path=str(TEST_VIDEO_PATH),
        episode=1,
        name="test 114",
        uploader="TensoRaws",
    )

    name = gen_file_name(anime_info=anime_info)
    assert name == "[TensoRaws] test 114 [01] [WEBRip 144p AVC-8bit AAC].mp4"

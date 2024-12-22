import shutil

from animepipeline.mediainfo import gen_file_name, get_media_info, rename_file
from animepipeline.mediainfo.type import FileNameInfo

from .util import ASSETS_PATH, TEST_VIDEO_PATH


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


def test_rename_file() -> None:
    # copy TEST_VIDEO_PATH to a new file
    if not (ASSETS_PATH / "copy_test_144p.mp4").exists():
        shutil.copy(TEST_VIDEO_PATH, ASSETS_PATH / "copy_test_144p.mp4")

    anime_info = FileNameInfo(
        path=str(ASSETS_PATH / "copy_test_144p.mp4"),
        episode=1,
        name="test 114",
        uploader="TensoRaws",
    )

    p = rename_file(anime_info=anime_info)
    assert p.name == "[TensoRaws] test 114 [01] [WEBRip 144p AVC-8bit AAC].mp4"

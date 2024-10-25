from animepipeline.mediainfo.gen_file_name import gen_file_name
from animepipeline.mediainfo.type import FileNameInfo

from .util import TEST_VIDEO_PATH


def test_gen_file_name() -> None:
    anime_info = FileNameInfo(
        path=str(TEST_VIDEO_PATH),
        episode=1,
        name="test 114",
        uploader="TensoRaws",
    )

    name = gen_file_name(anime_info=anime_info)
    assert name == "[TensoRaws] test 114 [01] [144p AVC-8bit AAC].mp4"

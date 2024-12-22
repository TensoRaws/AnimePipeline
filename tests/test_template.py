from animepipeline.template import get_bangumi_info, get_media_info_block

from .util import TEST_VIDEO_PATH


def test_get_media_info_block() -> None:
    print("\n")
    media_info_block = get_media_info_block(video_path=TEST_VIDEO_PATH)
    print(media_info_block)


def test_get_bangumi_info() -> None:
    summary, chinese_name = get_bangumi_info(bangumi_url="https://bangumi.tv/subject/464376")
    print(chinese_name)
    print("\n ---------------------------------- \n")
    print(summary)

from animepipeline.template import gen_media_info_block

from .util import TEST_VIDEO_PATH


def test_gen_media_info_block() -> None:
    print("\n")
    media_info_block = gen_media_info_block(video_path=TEST_VIDEO_PATH)
    print(media_info_block)

from animepipeline.template import PostTemplate, get_bangumi_info, get_media_info_block

from .util import TEST_VIDEO_PATH


def test_get_media_info_block() -> None:
    print("\n")
    media_info_block = get_media_info_block(video_path=TEST_VIDEO_PATH)
    print(media_info_block)


def test_get_bangumi_info() -> None:
    summary, chinese_name = get_bangumi_info(bangumi_url="https://bgm.tv/subject/454684")
    print(chinese_name)
    print("\n ---------------------------------- \n")
    print(summary)


def test_post_template() -> None:
    post_template = PostTemplate(
        video_path=TEST_VIDEO_PATH,
        bangumi_url="https://bgm.tv/subject/454684",
        chinese_name="BanG Dream! Ave Mujica",
        uploader="TensoRaws",
    )
    print(post_template.html())
    print(post_template.markdown())
    print(post_template.bbcode())

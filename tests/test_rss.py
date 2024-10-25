from animepipeline.config import NyaaConfig
from animepipeline.rss.nyaa import parse_nyaa


def test_parse_nyaa() -> None:
    # 测试解析nyaa rss
    res = parse_nyaa(
        NyaaConfig(
            name="Make Heroine ga Oosugiru!",
            translation="败犬女主太多了！",
            bangumi="https://bangumi.tv/subject/464376",
            link="https://nyaa.si/?page=rss&q=%5BSubsPlease%5D+Make+Heroine+ga+Oosugiru%21+-++%281080p%29&c=0_0&f=0",
            pattern=r"Make Heroine ga Oosugiru! - (\d+) \(1080p\)",
        ),
    )
    print(res)
    assert len(res) > 0

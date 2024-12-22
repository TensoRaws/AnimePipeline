from pathlib import Path
from typing import List, Optional, Union

from animepipeline.template.bangumi import get_bangumi_info
from animepipeline.template.mediainfo import get_media_info_block
from animepipeline.util import gen_magnet_link


def get_telegram_text(chinese_name: str, episode: int, file_name: str, torrent_file_hash: str) -> str:
    """
    Get telegram text.

    :param chinese_name: Chinese name
    :param episode: Episode
    :param file_name: File name
    :param torrent_file_hash: Torrent file hash
    """
    telegram_text = f"""
✈️ -----> 正在出种...
{chinese_name} | EP {str(episode).zfill(2)}
{file_name}
磁力链接 | Magnet Link:

{gen_magnet_link(torrent_file_hash)}

"""
    return telegram_text


class PostTemplate:
    def __init__(
        self,
        video_path: Union[str, Path],
        bangumi_url: str,
        chinese_name: Optional[str] = None,
        uploader: str = "TensoRaws",
        announcement: Optional[str] = None,
        adivertisement_images: Optional[List[str]] = None,
    ) -> None:
        """
        Initialize post template.

        :param video_path: Video path
        :param bangumi_url: Bangumi URL
        :param chinese_name: Chinese name, default is None (auto fetch from bangumi_url)
        :param uploader: Uploader
        :param announcement: Announcement string
        :param adivertisement_images: Adivertisement images, required at least 3 images, Recruitment, Telegram Group, Telegram Channel images
        """
        if adivertisement_images is not None and len(adivertisement_images) < 3:
            raise ValueError(
                "Adivertisement images required at least 3 images, Recruitment, Telegram Group, Telegram Channel images"
            )

        self.video_path = video_path
        self.uploader = uploader

        self.media_info_block = get_media_info_block(video_path=self.video_path, uploader=self.uploader)

        self.bangumi_url = bangumi_url
        self.summary, self.chinese_name = get_bangumi_info(bangumi_url=self.bangumi_url, chinese_name=chinese_name)

        if announcement is not None:
            self.announcement = announcement
        else:
            self.announcement = """片源来源于网络，感谢原资源提供者！
本资源使用 FinalRip 分布式压制。

Resources are from the internet, thanks to the original providers!
Using FinalRip for distributed video processing."""

        if adivertisement_images is not None:
            self.adivertisement_images = adivertisement_images
        else:
            # 招新海报，电报群，电报频道
            self.adivertisement_images = [
                "https://raw.githubusercontent.com/TensoRaws/.github/refs/heads/main/TensoRaws%E6%8B%9B%E6%96%B0.jpg",
                "https://raw.githubusercontent.com/TensoRaws/.github/refs/heads/main/TensoRaws%E7%94%B5%E6%8A%A5%E7%BE%A4.png",
                "https://raw.githubusercontent.com/TensoRaws/.github/refs/heads/main/TensoRaws%E7%94%B5%E6%8A%A5%E9%A2%91%E9%81%93.png",
            ]

    def html(self) -> str:
        advertisement_images_block = "\n".join([f'<img src="{url}" width=250 />' for url in self.adivertisement_images])

        return f"""
<div>
    <h3>Announcement:</h3>
    <pre style="font-family: 'Courier New', Courier, monospace;">{self.announcement}</pre>
    <br />
    <h4>{self.chinese_name}</h4>
    <p><b>Story: </b></p>
    <pre style="font-family: 'Courier New', Courier, monospace;">{self.summary}</pre>
    <br />
    <h4>MediaInfo:</h4>
    <pre style="font-family: 'Courier New', Courier, monospace;">{self.media_info_block}</pre>
    <br />
    {advertisement_images_block}
</div>
"""

    def markdown(self) -> str:
        return f"""### Announcement:
```
{self.announcement}
```

### {self.chinese_name}
Story:
{self.summary}

### MediaInfo:
```
{self.media_info_block}
```

[招新链接 | Recruitment Link]({self.adivertisement_images[0]})

[电报群链接 | Telegram Group Link]({self.adivertisement_images[1]})

[电报频道链接 | Telegram Channel Link]({self.adivertisement_images[2]})
"""

    def bbcode(self) -> str:
        advertisement_images_block = "\n".join(
            [f"[url={url}][img]{url}[/img][/url]" for url in self.adivertisement_images]
        )

        return f"""[quote][b]Announcement:[size=3]
{self.announcement}
[/size]
[/b][/quote]

[b][size=4]{self.chinese_name}[/size][/b]
[b]Story: [/b]
{self.summary}

[quote][font=Courier New]
[b]MediaInfo: [/b]
{self.media_info_block}
[/font][/quote]

{advertisement_images_block}
"""

    def save(
        self,
        html_path: Optional[Union[str, Path]],
        markdown_path: Optional[Union[str, Path]],
        bbcode_path: Optional[Union[str, Path]],
    ) -> None:
        """
        Save the post template to file.

        :param html_path: HTML file path
        :param markdown_path: Markdown file path
        :param bbcode_path: BBCode file path
        """
        if html_path is not None:
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(self.html())

        if markdown_path is not None:
            with open(markdown_path, "w", encoding="utf-8") as f:
                f.write(self.markdown())

        if bbcode_path is not None:
            with open(bbcode_path, "w", encoding="utf-8") as f:
                f.write(self.bbcode())

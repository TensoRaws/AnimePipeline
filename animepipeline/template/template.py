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
        video_path: str,
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
        :param adivertisement_images: Adivertisement images
        """
        self.video_path = video_path
        self.uploader = uploader

        self.media_info_block = get_media_info_block(video_path=self.video_path, uploader=self.uploader)

        self.bangumi_url = bangumi_url
        self.summary, self.chinese_name = get_bangumi_info(bangumi_url=self.bangumi_url, chinese_name=chinese_name)

        if announcement is not None:
            self.announcement = announcement
        else:
            self.announcement = """
资源来源于网络，感谢原资源提供者！
本资源使用 FinalRip 分布式压制。

Resources are from the internet, thanks to the original providers!
Using FinalRip for distributed video processing.
"""

        if adivertisement_images is not None:
            self.adivertisement_images = adivertisement_images
        else:
            # 招新海报，电报群，电报频道
            self.adivertisement_images = [
                "https://raw.githubusercontent.com/TensoRaws/.github/refs/heads/main/TensoRaws%E6%8B%9B%E6%96%B0.jpg",
                "https://raw.githubusercontent.com/TensoRaws/.github/refs/heads/main/TensoRaws%E7%94%B5%E6%8A%A5%E7%BE%A4.png",
                "https://raw.githubusercontent.com/TensoRaws/.github/refs/heads/main/TensoRaws%E7%94%B5%E6%8A%A5%E9%A2%91%E9%81%93.png",
            ]

    # def html(self) -> str:
    #     pass
    #
    # def markdown(self) -> str:
    #     pass
    #
    # def bbcode(self) -> str:
    #     pass

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
        pass

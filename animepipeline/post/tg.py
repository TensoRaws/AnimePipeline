from pathlib import Path
from typing import Optional, Union

import telegram.error
from loguru import logger
from telegram import Bot

from animepipeline.config import TelegramConfig


class TGChannelSender:
    """
    TG Channel Sender.

    :param config: The telegram configuration.
    """

    def __init__(self, config: TelegramConfig) -> None:
        if config.local_mode:
            self.bot = Bot(
                token=config.bot_token,
                base_url=str(config.base_url),
                base_file_url=str(config.base_file_url),
                local_mode=True,
            )
        else:
            self.bot = Bot(token=config.bot_token)

        self.channel_id = config.channel_id

    async def send_video(self, video_path: Union[Path, str], caption: Optional[str] = None) -> None:
        """
        Send video to the channel.

        :param video_path:
        :param caption: the caption of the video
        """
        video_path = Path(video_path)
        video_name = video_path.name
        if not video_path.exists():
            raise FileNotFoundError(f"Video file not found: {video_path}")

        if caption is None:
            caption = video_name

        with open(video_path, "rb") as f:
            video_file = f.read()

        try:
            await self.bot.send_video(
                chat_id=self.channel_id,
                video=video_file,
                filename=video_name,
                caption=caption,
                read_timeout=6000,
                write_timeout=6000,
            )
        except telegram.error.NetworkError as e:
            logger.error(f"Network error: {e}, video path: {video_path}, video_caption: {caption}")
        except Exception as e:
            logger.error(f"Unknown Error sending video: {e}, video path: {video_path}, video_caption: {caption}")

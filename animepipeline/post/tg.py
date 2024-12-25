import telegram
from loguru import logger
from telegram import Bot
from tenacity import retry, stop_after_attempt, wait_random

from animepipeline.config import TelegramConfig


class TGChannelSender:
    """
    TG Channel Sender.

    :param config: The telegram configuration.
    """

    def __init__(self, config: TelegramConfig) -> None:
        self.bot = Bot(token=config.bot_token)
        self.channel_id = config.channel_id

    @retry(wait=wait_random(min=3, max=15), stop=stop_after_attempt(10))
    async def send_text(self, text: str) -> None:
        """
        Send text to the channel.

        :param text: The text to send.
        """
        try:
            await self.bot.send_message(
                chat_id=self.channel_id,
                text=text,
                read_timeout=60,
                write_timeout=60,
                connect_timeout=60,
                pool_timeout=600,
            )
        except telegram.error.NetworkError as e:
            logger.error(f"Network error: {e}, text: {text}")
            raise e
        except Exception as e:
            logger.error(f"Unknown Error sending text: {e}, text: {text}")

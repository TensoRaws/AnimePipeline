import os

import pytest

from animepipeline.config import ServerConfig
from animepipeline.post.tg import TGChannelSender
from animepipeline.template import get_telegram_text

from .util import CONFIG_PATH


@pytest.mark.skipif(os.environ.get("GITHUB_ACTIONS") == "true", reason="Only test locally")
async def test_tg_bot() -> None:
    server_config: ServerConfig = ServerConfig.from_yaml(CONFIG_PATH / "server.yml")

    sender = TGChannelSender(server_config.telegram)

    await sender.send_text(
        text=get_telegram_text(
            chinese_name="from unit test ~~~  |  败犬女主太多了！",
            episode=2,
            file_name="[TensoRaws] Make Heroine ga Oosugiru! [02] [1080p AVC-8bit FLAC].mkv",
            torrent_file_hash="this_is_a_fake_hash",
        )
    )

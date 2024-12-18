import os

import pytest

from animepipeline.config import ServerConfig
from animepipeline.post.tg import TGChannelSender

from .util import CONFIG_PATH

video_key = "test_144p.mp4"


@pytest.mark.skipif(os.environ.get("GITHUB_ACTIONS") == "true", reason="Only test locally")
async def test_tg_bot() -> None:
    server_config: ServerConfig = ServerConfig.from_yaml(CONFIG_PATH / "server.yml")

    video_sender = TGChannelSender(server_config.telegram)

    await video_sender.send_text(text="from unit test --> | 114514 哼哼啊啊啊 | test.mp4")

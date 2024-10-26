import asyncio
import os

import pytest

from animepipeline.config import RSSConfig, ServerConfig
from animepipeline.encode.finalrip import FinalRipClient
from animepipeline.encode.type import GetTaskProgressRequest, TaskNotCompletedError

from .util import ASSETS_PATH, CONFIG_PATH

video_key = "test_144p.mp4"


@pytest.mark.asyncio
@pytest.mark.skipif(os.environ.get("GITHUB_ACTIONS") == "true", reason="Only test locally")
class Test_FinalRip:
    def setup_method(self) -> None:
        server_config: ServerConfig = ServerConfig.from_yaml(CONFIG_PATH / "server.yml")
        self.finalrip = FinalRipClient(server_config.finalrip)

    async def test_ping(self) -> None:
        ping_response = await self.finalrip.ping()
        print(ping_response)

    async def test_new_task(self) -> None:
        await self.finalrip.upload_and_new_task(ASSETS_PATH / video_key)

    async def test_start_task(self) -> None:
        rss_config: RSSConfig = RSSConfig.from_yaml(CONFIG_PATH / "rss.yml")

        p: str = ""
        for _, v in rss_config.params.items():
            p = v
        print(repr(p))
        s: str = ""
        for _, v in rss_config.scripts.items():
            s = v
        print(repr(s))
        try:
            await self.finalrip.start_task(encode_param=p, script=s, video_key=video_key)
        except Exception as e:
            print(e)

    async def test_check_task_exist(self) -> None:
        assert await self.finalrip.check_task_exist(video_key)

    async def test_check_task_completed(self) -> None:
        print(await self.finalrip.check_task_completed(video_key))

    async def test_task_progress(self) -> None:
        task_progress = await self.finalrip._get_task_progress(GetTaskProgressRequest(video_key=video_key))
        print(task_progress)

    async def test_retry_merge(self) -> None:
        await self.finalrip.retry_merge(video_key)

    async def test_download_completed_task(self) -> None:
        while True:
            try:
                await self.finalrip.download_completed_task(video_key=video_key, save_path=ASSETS_PATH / "encode.mkv")
                break
            except TaskNotCompletedError:
                print("Task not completed yet")
                await asyncio.sleep(5)
            except Exception as e:
                print(e)
                await asyncio.sleep(5)

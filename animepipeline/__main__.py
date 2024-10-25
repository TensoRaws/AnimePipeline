import asyncio
from pathlib import Path

from animepipeline import AsyncJsonStore, Loop, RSSConfig, ServerConfig

CONFIG_PATH = Path(__file__).resolve().parent.parent.absolute() / "conf"


async def main() -> None:
    server_config: ServerConfig = ServerConfig.from_yaml(CONFIG_PATH / "server.yml")
    rss_config: RSSConfig = RSSConfig.from_yaml(CONFIG_PATH / "rss.yml")
    json_store = AsyncJsonStore(CONFIG_PATH / "store.json")
    loop = Loop(server_config=server_config, rss_config=rss_config, json_store=json_store)
    await loop.start()


if __name__ == "__main__":
    asyncio.run(main())

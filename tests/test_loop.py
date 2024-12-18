from animepipeline.config import RSSConfig, ServerConfig
from animepipeline.loop import TaskInfo, build_task_info
from animepipeline.rss import parse_nyaa

from .util import CONFIG_PATH


def test_build_task_info() -> None:
    rss_config: RSSConfig = RSSConfig.from_yaml(CONFIG_PATH / "rss.yml")
    server_config: ServerConfig = ServerConfig.from_yaml(CONFIG_PATH / "server.yml")
    for cfg in rss_config.nyaa:
        torrent_info_list = parse_nyaa(cfg)

        for torrent_info in torrent_info_list:
            task_info = build_task_info(torrent_info, cfg, rss_config, server_config)
            assert isinstance(task_info, TaskInfo)
            print(task_info)

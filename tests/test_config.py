from animepipeline.config.rss import RSSConfig
from animepipeline.config.server import ServerConfig

from .util import CONFIG_PATH


def test_load_server_config() -> None:
    # 使用 from_yaml 加载配置
    server_config: ServerConfig = ServerConfig.from_yaml(CONFIG_PATH / "server.yml")
    print(server_config)


def test_load_rss_config() -> None:
    # 使用 from_yaml 加载配置
    rss_config: RSSConfig = RSSConfig.from_yaml(CONFIG_PATH / "rss.yml")
    print(rss_config)
    # time.sleep(5)
    # 使用 refresh_config 刷新配置
    rss_config.refresh_config()
    print(rss_config)
    # test get script
    script_name = rss_config.nyaa[0].script
    assert isinstance(script_name, str)

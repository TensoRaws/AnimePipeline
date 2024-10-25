import os
from pathlib import Path
from typing import Any, Union

import yaml
from pydantic import AnyUrl, BaseModel, DirectoryPath, Field, ValidationError


class LoopConfig(BaseModel):
    interval: int


class QBitTorrentConfig(BaseModel):
    host: str
    port: int = Field(..., ge=1, le=65535)
    username: Union[str, int]
    password: Union[str, int]
    download_path: DirectoryPath


class FinalRipConfig(BaseModel):
    url: AnyUrl
    token: Union[str, int]


class TelegramConfig(BaseModel):
    enable: bool
    local_mode: bool
    base_url: AnyUrl
    base_file_url: AnyUrl
    bot_token: str
    channel_id: Union[str, int]


class ServerConfig(BaseModel):
    loop: LoopConfig
    qbittorrent: QBitTorrentConfig
    finalrip: FinalRipConfig
    telegram: TelegramConfig

    @classmethod
    def from_yaml(cls, path: Union[Path, str]) -> Any:
        """
        Load configuration from a YAML file.

        :param path: The path to the yaml file.
        """
        if not os.path.exists(path):
            raise FileNotFoundError(f"Config file {path} not found")
        with open(path, "r", encoding="utf-8") as file:
            try:
                config_data = yaml.safe_load(file)
            except yaml.YAMLError as e:
                raise ValueError(f"Error loading YAML: {e}")
            except ValidationError as e:
                raise ValueError(f"Config validation error: {e}")
            except Exception as e:
                raise ValueError(f"Error loading config: {e}")

        config = cls(**config_data)

        return config

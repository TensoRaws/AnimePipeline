import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import yaml
from pydantic import AnyUrl, BaseModel, DirectoryPath, FilePath, ValidationError


class BaseConfig(BaseModel):
    uploader: str
    script: str
    param: str


class NyaaConfig(BaseModel):
    name: str
    translation: str
    bangumi: Union[str, AnyUrl]
    link: Union[str, AnyUrl]
    pattern: str
    uploader: Optional[str] = None
    script: Optional[str] = None
    param: Optional[str] = None


class RSSConfig(BaseModel):
    base: BaseConfig
    nyaa: List[NyaaConfig]
    scripts: Dict[str, str]
    params: Dict[str, str]

    config_path: Optional[FilePath] = None
    scripts_path: Optional[DirectoryPath] = None
    params_path: Optional[DirectoryPath] = None

    @classmethod
    def from_yaml(
        cls,
        path: Union[Path, str],
        scripts_path: Optional[Union[Path, str]] = None,
        params_path: Optional[Union[Path, str]] = None,
    ) -> Any:
        """
        Load configuration from a YAML file.

        :param path: The path to the yaml file.
        :param scripts_path: The path to the folder containing scripts files (xx.py).
        :param params_path: The path to the folder containing params files (xx.txt).
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

        def _gen_dict(folder_path: Union[Path, str]) -> Dict[str, str]:
            """
            Generate a dictionary from the files in the folder. file_name -> file_content.

            :param folder_path: The path to the folder.
            """
            if not os.path.exists(folder_path):
                raise FileNotFoundError(f"Folder {folder_path} not found")
            res = {}
            for _file in os.listdir(folder_path):
                with open(os.path.join(folder_path, _file), "r", encoding="utf-8") as f:
                    res[_file] = f.read()

                # remove newline symbol at the end
                # cuz the encode param will be passed to the server, that will directly "param" + "encode.mkv"
                # if there is a newline symbol at the end, the server will not find the file
                if res[_file].endswith("\n"):
                    res[_file] = res[_file][:-1]
                elif res[_file].endswith("\r\n"):
                    res[_file] = res[_file][:-2]
                elif res[_file].endswith("\r"):
                    res[_file] = res[_file][:-1]

            return res

        if scripts_path is None:
            scripts_path = os.path.join(os.path.dirname(path), "scripts")

        if params_path is None:
            params_path = os.path.join(os.path.dirname(path), "params")

        config_data["scripts"] = _gen_dict(scripts_path)
        config_data["params"] = _gen_dict(params_path)

        config = cls(**config_data)

        # validate the config
        # base
        if config.base.script not in config.scripts:
            raise ValueError(f"base: script {config.base.script} not found")

        if config.base.param not in config.params:
            raise ValueError(f"base: param {config.base.param} not found")

        # nyaa
        for item in config.nyaa:
            if item.uploader is None:
                item.uploader = config.base.uploader

            if item.script is None:
                item.script = config.base.script
            else:
                if item.script not in config.scripts:
                    raise ValueError(f"nyaa: script {item.script} not found")

            if item.param is None:
                item.param = config.base.param
            else:
                if item.param not in config.params:
                    raise ValueError(f"nyaa: param {item.param} not found")

        config.config_path = Path(path)
        config.scripts_path = Path(scripts_path)
        config.params_path = Path(params_path)

        return config

    def refresh_config(self) -> None:
        """
        Refresh configuration from the yaml file.
        """
        try:
            if self.config_path is None:
                raise ValueError("No configuration file path provided")
            new_config = RSSConfig.from_yaml(self.config_path, self.scripts_path, self.params_path)
        except Exception as e:
            print(f"Failed to load new configuration: {e}")
            return

        self.base = new_config.base
        self.nyaa = new_config.nyaa
        self.scripts = new_config.scripts
        self.params = new_config.params

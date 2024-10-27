# AnimePipeline

auto encode new anime episode, driven by [**FinalRip**](https://github.com/TensoRaws/FinalRip)

[![codecov](https://codecov.io/gh/TensoRaws/AnimePipeline/graph/badge.svg?token=CtgLouRy8u)](https://codecov.io/gh/TensoRaws/AnimePipeline)
[![CI-test](https://github.com/TensoRaws/AnimePipeline/actions/workflows/CI-test.yml/badge.svg)](https://github.com/TensoRaws/AnimePipeline/actions/workflows/CI-test.yml)
[![Docker Build CI](https://github.com/TensoRaws/AnimePipeline/actions/workflows/CI-docker.yml/badge.svg)](https://github.com/TensoRaws/AnimePipeline/actions/workflows/CI-docker.yml)
[![Release](https://github.com/TensoRaws/AnimePipeline/actions/workflows/Release.yml/badge.svg)](https://github.com/TensoRaws/AnimePipeline/actions/workflows/Release.yml)
[![PyPI version](https://badge.fury.io/py/animepipeline.svg)](https://badge.fury.io/py/animepipeline)
![GitHub](https://img.shields.io/github/license/TensoRaws/AnimePipeline)

### Architecture

![AnimePipeline](https://raw.githubusercontent.com/TensoRaws/.github/refs/heads/main/animepipeline.png)

### Installation

FinalRip is required, if you don't familiar with it, please play with it first.

Python 3.9 or higher is required, we use poetry to manage dependencies.

btw, `make` is required to run the commands in the `Makefile`.

```bash
poetry install
make run
```

or you can use docker to run the project, see [docker-compose.yml](./deploy/docker-compose.yml) for more details.

### Configuration

#### Server Config:

- loop interval: the interval of the loop, default is 200s
- _download path_: the path to save the downloaded torrent file, if you use docker, you should mount the volume to the container, then use the path in the container. like `/downloads`
- telegram bot token & channel id: your own bot token and channel id
- telegram bot api: use tg bot local mode, see [telegram-bot-api](https://core.telegram.org/api/obtaining_api_id) for more details.

#### RSS Config:

you should provide the compatible params and scripts in the [params](./conf/params) and [scripts](./conf/scripts) folder.

**the file name will be used as the key**

- base: the default settings, can be overridden in the rss list
- link: the rss link, make sure it's a valid rss link
- pattern: to match the episode(int), use regex

### Reference

- [**FinalRip**](https://github.com/TensoRaws/FinalRip)
- [FFmpeg](https://github.com/FFmpeg/FFmpeg)
- [VapourSynth](https://github.com/vapoursynth/vapoursynth)
- [asyncio](https://docs.python.org/3/library/asyncio.html)
- [httpx](https://github.com/encode/httpx)
- [qbittorrent](https://github.com/qbittorrent/qBittorrent)
- [qbittorrent-api](https://github.com/rmartin16/qbittorrent-api)
- [telegram-bot-api](https://github.com/tdlib/telegram-bot-api)
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)

### License

This project is licensed under the GPL-3.0 license - see the [LICENSE file](https://github.com/TensoRaws/AnimePipeline/blob/main/LICENSE) for details.

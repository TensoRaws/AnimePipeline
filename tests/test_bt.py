import os
import shutil
import time
from pathlib import Path

import pytest

from animepipeline.bt.qb import QBittorrentManager
from animepipeline.config import ServerConfig

from .util import CONFIG_PATH, TEST_VIDEO_PATH


@pytest.mark.skipif(
    os.environ.get("GITHUB_ACTIONS") == "true", reason="Only test locally cuz BT may not suitable for CI"
)
def test_qbittorrent() -> None:
    torrent_hash = "5484cff30b108ca1d1987fb6ea4eebed356b9ddd"
    torrent_url = "https://nyaa.si/download/1878677.torrent"

    if Path("../deploy/docker/downloads").exists():
        download_path = Path("../deploy/docker/downloads")
    else:
        download_path = Path("./deploy/docker/downloads")

    server_config: ServerConfig = ServerConfig.from_yaml(CONFIG_PATH / "server.yml")
    cfg = server_config.qbittorrent
    cfg.download_path = download_path.absolute()
    qb_manager = QBittorrentManager(config=cfg)

    qb_manager.add_torrent(torrent_hash=torrent_hash, torrent_url=torrent_url)

    # Check if the download is complete
    while True:
        time.sleep(5)
        if qb_manager.check_download_complete(torrent_hash):
            print("Download is complete.")
            break
        else:
            print("Download is not complete.")

    # Get the downloaded filename
    file_path = qb_manager.get_downloaded_path(torrent_hash)
    if file_path is not None:
        print(f"Downloaded file: {file_path}")
    else:
        print("Download is not complete or failed.")

    h = QBittorrentManager.make_torrent_file(
        file_path=TEST_VIDEO_PATH,
        torrent_file_save_path=download_path / "test_144p.torrent",
    )
    print(f"Torrent hash: {h}")

    # copy the torrent file to the download path
    shutil.copy(TEST_VIDEO_PATH, download_path)

    qb_manager.add_torrent(torrent_hash=h, torrent_file_path=download_path / "test_144p.torrent")

    # Check if the reseed is complete
    while True:
        time.sleep(2)
        if qb_manager.check_download_complete(torrent_hash):
            print("Reseed is complete.")
            break
        else:
            print("Reseed is not complete.")

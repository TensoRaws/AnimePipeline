from pathlib import Path
from typing import List, Optional, Tuple, Union

import qbittorrentapi
from loguru import logger

from animepipeline.config import QBitTorrentConfig
from animepipeline.util import gen_magnet_link


class QBittorrentManager:
    """
    QBittorrent manager

    :param config: QBitTorrentConfig object
    """

    def __init__(self, config: QBitTorrentConfig) -> None:
        self.client = qbittorrentapi.Client(
            host=config.host,
            port=config.port,
            username=config.username,
            password=config.password,
        )

        self.download_path = config.download_path

        self.COMPLETE_STATES = ["uploading", "stalledUP", "pausedUP", "queuedUP"]

    def add_torrent(self, torrent_hash: str, torrent_url: Optional[Union[str, Path]] = None) -> None:
        """
        Add a torrent to download

        :param torrent_hash: Torrent hash
        :param torrent_url: Torrent URL, defaults to None, in which case a magnet link will be
        """
        if torrent_url is None:
            torrent_url = gen_magnet_link(torrent_hash)

        if self.check_torrent_exist(torrent_hash):
            logger.warning(f"Torrent {torrent_hash} already exists.")
            return

        try:
            self.client.torrents.add(urls=torrent_url)
            logger.info(f"Torrent {torrent_url} added for download.")
        except Exception as e:
            logger.error(f"Failed to add torrent: {e}")

    def check_download_complete(self, torrent_hash: str) -> bool:
        """
        Check if the download is complete

        :param torrent_hash: Torrent hash
        """

        try:
            torrent = self.client.torrents_info(torrent_hashes=torrent_hash)

            if torrent[0].state in self.COMPLETE_STATES:
                return True
            else:
                return False

        except Exception as e:
            logger.error(f"Error checking download status: {e}")
            return False

    def get_downloaded_path(self, torrent_hash: str) -> Optional[Path]:
        """
        Get the downloaded path of the torrent, only return the largest file if multiple files are present.

        :param torrent_hash:
        """
        try:
            torrent = self.client.torrents_info(torrent_hashes=torrent_hash)

            if torrent[0].state in self.COMPLETE_STATES:
                file_list: List[Tuple[str, int]] = [(file["name"], file["size"]) for file in torrent[0].files]
                file_list.sort(key=lambda x: x[1], reverse=True)
                return self.download_path / Path(file_list[0][0])

            else:
                return None

        except Exception as e:
            logger.error(f"Error getting filename: {e}")
            return None

    def check_torrent_exist(self, torrent_hash: str) -> bool:
        """
        Check if the torrent exists in the download list

        :param torrent_hash: Torrent hash
        """
        try:
            torrent = self.client.torrents_info(torrent_hashes=torrent_hash)
            return len(torrent) > 0

        except Exception as e:
            logger.error(f"Error checking torrent existence: {e}")
            return False

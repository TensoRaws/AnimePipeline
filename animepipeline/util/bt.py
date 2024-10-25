def gen_magnet_link(torrent_hash: str) -> str:
    """
    Generate a magnet link from a torrent hash.

    :param torrent_hash: The torrent hash.
    """
    return f"magnet:?xt=urn:btih:{torrent_hash}"

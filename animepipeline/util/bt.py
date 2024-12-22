def gen_magnet_link(torrent_hash: str) -> str:
    """
    Generate a magnet link from a torrent hash.

    :param torrent_hash: The torrent hash.
    """
    return f"magnet:?xt=urn:btih:{torrent_hash}"


# bt tracker urls
ANNOUNCE_URLS = [
    "http://nyaa.tracker.wf:7777/announce",
    "http://open.acgtracker.com:1096/announce",
    "http://t.nyaatracker.com:80/announce",
    "http://tracker4.itzmx.com:2710/announce",
    "https://tracker.nanoha.org/announce",
    "http://t.acg.rip:6699/announce",
    "https://tr.bangumi.moe:9696/announce",
    "http://tr.bangumi.moe:6969/announce",
    "udp://tr.bangumi.moe:6969/announce",
    "http://open.acgnxtracker.com/announce",
    "https://open.acgnxtracker.com/announce",
    "udp://open.stealth.si:80/announce",
    "udp://tracker.opentrackr.org:1337/announce",
    "udp://exodus.desync.com:6969/announce",
    "udp://tracker.torrent.eu.org:451/announce",
    "udp://tracker.openbittorrent.com:80/announce",
    "udp://tracker.publicbt.com:80/announce",
    "udp://tracker.prq.to:80/announce",
    "udp://104.238.198.186:8000/announce",
    "http://104.238.198.186:8000/announce",
    "http://94.228.192.98/announce",
    "http://share.dmhy.org/annonuce",
    "http://tracker.btcake.com/announce",
    "http://tracker.ktxp.com:6868/announce",
    "http://tracker.ktxp.com:7070/announce",
    "http://bt.sc-ol.com:2710/announce",
    "http://btfile.sdo.com:6961/announce",
    "https://t-115.rhcloud.com/only_for_ylbud",
    "http://exodus.desync.com:6969/announce",
    "udp://coppersurfer.tk:6969/announce",
    "http://tracker3.torrentino.com/announce",
    "http://tracker2.torrentino.com/announce",
    "udp://open.demonii.com:1337/announce",
    "udp://tracker.ex.ua:80/announce",
    "http://pubt.net:2710/announce",
    "http://tracker.tfile.me/announce",
    "http://bigfoot1942.sektori.org:6969/announce",
    "udp://bt.sc-ol.com:2710/announce",
    "http://1337.abcvg.info:80/announce",
    "http://bt.okmp3.ru:2710/announce",
    "http://ipv6.rer.lol:6969/announce",
    "https://tr.burnabyhighstar.com:443/announce",
    "https://tracker.gbitt.info:443/announce",
    "https://tracker.gcrenwp.top:443/announce",
    "https://tracker.kuroy.me:443/announce",
    "https://tracker.lilithraws.org:443/announce",
    "https://tracker.loligirl.cn:443/announce",
    "https://tracker1.520.jp:443/announce",
    "udp://amigacity.xyz:6969/announce",
    "udp://bt1.archive.org:6969/announce",
    "udp://bt2.archive.org:6969/announce",
    "udp://epider.me:6969/announce",
    "wss://tracker.openwebtorrent.com:443/announce",
]

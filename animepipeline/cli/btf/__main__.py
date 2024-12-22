import argparse
from pathlib import Path

from loguru import logger

from animepipeline.bt import QBittorrentManager
from animepipeline.template import PostTemplate

parser = argparse.ArgumentParser(description="Generate all post info files for the anime.")

# Input Path
parser.add_argument("-p", "--PATH", help="Path to the video file", required=True)
# Bangumi URL
parser.add_argument("-b", "--BANGUMI", help="Bangumi URL", required=True)
# Chinese Name
parser.add_argument("-n", "--NAME", help="Chinese name", required=False)
# Uploader Name
parser.add_argument("-u", "--UPLOADER", help="Uploader name", required=False)
# Make Torrent
parser.add_argument("-t", "--TORRENT", help="file_path -> torrent", required=False)

args = parser.parse_args()


def main() -> None:
    if args.UPLOADER is None:
        args.UPLOADER = "TensoRaws"

    # Make torrent file
    if args.TORRENT is not None:
        file_path = Path(args.TORRENT)
        h = QBittorrentManager.make_torrent_file(
            file_path=file_path, torrent_file_save_path=file_path.name + ".torrent"
        )
        logger.info(f"Make torrent file success, hash: {h}")

    # Generate post info files
    path = Path(args.PATH)

    post_template = PostTemplate(
        video_path=path,
        bangumi_url=args.BANGUMI,
        chinese_name=args.NAME,
        uploader=args.UPLOADER,
    )

    post_template.save(
        html_path=path.name + ".html",
        markdown_path=path.name + ".md",
        bbcode_path=path.name + ".txt",
    )
    logger.info("Generate post info files success.")


if __name__ == "__main__":
    main()

import argparse
from pathlib import Path

from animepipeline.mediainfo import FileNameInfo, rename_file

parser = argparse.ArgumentParser(description="Rename anime video files")

# Input Path
parser.add_argument("-p", "--PATH", help="Path to the video file or directory", required=True)
# Episode Number
parser.add_argument("-e", "--EPISODE", help="Episode number", required=False)
# Anime Name
parser.add_argument("-n", "--NAME", help="Anime name", required=True)
# Uploader Name
parser.add_argument("-u", "--UPLOADER", help="Uploader name", required=False)

args = parser.parse_args()


def main() -> None:
    # TODO: Support withdraw of renaming

    if args.UPLOADER is None:
        args.UPLOADER = "TensoRaws"
    path = Path(args.PATH)

    if not path.is_dir():
        if args.EPISODE is None:
            raise ValueError("Episode number is required for single file")

        try:
            episode = int(args.EPISODE)
        except ValueError:
            raise ValueError("Episode number must be an integer")

        anime_info = FileNameInfo(
            path=path,
            episode=episode,
            name=args.NAME,
            uploader=args.UPLOADER,
        )
        new_path = rename_file(anime_info=anime_info)
        print(f"Renamed: {path} -> {new_path}")
    else:
        # TODO: Rename all video in the directory
        raise NotImplementedError("Not implemented yet")


if __name__ == "__main__":
    main()

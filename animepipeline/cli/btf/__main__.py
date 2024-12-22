import argparse
from pathlib import Path

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

args = parser.parse_args()


def main() -> None:
    if args.UPLOADER is None:
        args.UPLOADER = "TensoRaws"

    path = Path(args.PATH)

    post_template = PostTemplate(
        video_path=path,
        bangumi_url=args.BANGUMI,
        chinese_name=args.NAME,
        uploader=args.UPLOADER,
    )

    post_template.save(
        html_path=path.parent / (path.name + ".html"),
        markdown_path=path.parent / (path.name + ".md"),
        bbcode_path=path.parent / (path.name + ".txt"),
    )


if __name__ == "__main__":
    main()

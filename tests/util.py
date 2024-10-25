from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parent.parent.absolute() / "conf"
ASSETS_PATH = Path(__file__).resolve().parent.parent.absolute() / "assets"
TEST_VIDEO_PATH = ASSETS_PATH / "test_144p.mp4"

print(TEST_VIDEO_PATH)

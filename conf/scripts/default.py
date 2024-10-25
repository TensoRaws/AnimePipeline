import os

from vapoursynth import core

if os.getenv("FINALRIP_SOURCE"):
    clip = core.bs.VideoSource(source=os.getenv("FINALRIP_SOURCE"))
else:
    clip = core.bs.VideoSource(source="s.mkv")

clip.set_output()

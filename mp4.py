"""
Convert GIF to MP4

Using previously created unique GIF from ``gif.py`` is a quick and effortless way to
produce MP4 videos.
"""
import hashlib
import datetime

from pathlib import Path

import humanize

import ffmpy

VAR_PATH = Path("./var").resolve()
BUILD_PATH = VAR_PATH / "builds"
BUILD_GIF_PATH = BUILD_PATH / "gifs"
BUILD_MP4_PATH = BUILD_PATH / "mp4s"


def get_output_destination(source, destination):
    """
    Get the filename replace suffix with ".mp4" and locate it in given destination dir.
    """
    return BUILD_MP4_PATH / (source.stem + ".mp4")


if __name__ == "__main__":
    source_dir = Path("/home/thenonda/Essais/fake_gifs").resolve()
    destination_path = BUILD_MP4_PATH
    if not destination_path.exists():
        destination_path.mkdir(mode=0o777, parents=True)
    #sample_input = Path("/home/thenonda/Essais/fake_gifs/9259d606-36c0-4b48-a3a7-703bea1312b5_1.gif").resolve()

    for gif in source_dir.iterdir():
        get_output_destination(gif, BUILD_MP4_PATH)
        break

    #ff = ffmpy.FFmpeg(
        #inputs={sample_input: None},
        #outputs={sample_output: None}
    #)
    #ff.run()

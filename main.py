"""Entry point for the news-image-20261122 submission.

The platform runs this with the output directory as argv[1] and then reads
entry.png from inside that directory.  argv[1] is a directory, never a file
path: treating it as a filename is the easiest way to fail the gate.

The image is built by render.py, which needs Pillow and writes entry.png
beside this file.  This script has to run in the platform's sandbox, which
has the standard library and nothing else, so it copies the verified bytes
instead of drawing them again: a re-render there would need Pillow, and even
if it worked it could differ by a pixel from the image that was checked.

Standard library only.  No network.  No third-party packages.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
IMAGE_NAME = "entry.png"
OUTPUT_ENV = "MAKEFUN_OUTPUT_DIR"


def source_image():
    """The verified image that sits beside this script."""
    path = os.path.join(HERE, IMAGE_NAME)
    if not os.path.isfile(path):
        raise SystemExit(
            "missing %s beside main.py - run `python3 render.py entry.png` first"
            % IMAGE_NAME)
    return path


def target_dir(argv):
    """Resolve the output directory: argv[1], then the env var, then ./output."""
    if len(argv) > 1 and argv[1].strip():
        return argv[1].strip()
    for name in (OUTPUT_ENV, "OUTPUT_DIR"):
        value = os.environ.get(name, "").strip()
        if value:
            return value
    return os.path.join(os.getcwd(), "output")


def main(argv):
    out_dir = target_dir(argv)
    os.makedirs(out_dir, exist_ok=True)
    destination = os.path.join(out_dir, IMAGE_NAME)
    shutil.copyfile(source_image(), destination)
    print("wrote %s (%d bytes)" % (destination, os.path.getsize(destination)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

import glob
import argparse
import io
from pyexiv2 import Image
import pyavm
from PIL import Image
import re

def offset_from_microvideo(md):
    try:
        return int(md["Xmp.GCamera.MicroVideoOffset"])
    except KeyError:
        print(f"Skipping {filename}")
    return None

def offset_from_directory(md):
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pathname", type=str)
    parser.add_argument("--recursive", action="store_true")

    args = parser.parse_args()

    for filename in glob.iglob(args.pathname, recursive=args.recursive):
        print(filename)
        with open(filename, 'rb') as f:
            contents = f.read()
        start_motion_photo = [m.start() for m in re.finditer(b"Item:Semantic=\"MotionPhoto\"", contents)]
        if 0 == len(start_motion_photo):
            continue
        motion_length = [m for m in re.finditer(b"Item:Length=\"(\d+)\"", contents[start_motion_photo[0]:])]
        reverse_offset = motion_length[0].group(1)
        reverse_offset = int(reverse_offset)

        with open(filename, "rb") as f:
            f.seek(reverse_offset * -1, 2)
            rest_of_file = f.read()
            print(f.tell())
            with open(filename + ".mp4", "wb") as wf:
                wf.write(rest_of_file)
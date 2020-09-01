import glob
import argparse
import io
from pyexiv2 import Image

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pathname", type=str)
    parser.add_argument("--recursive", action="store_true")

    args = parser.parse_args()

    for filename in glob.iglob(args.pathname, recursive=args.recursive):
        print(filename)
        img = Image(filename)
        md = img.read_xmp()
        img.close()
        reverse_offset = int(md["Xmp.GCamera.MicroVideoOffset"])

        with open(filename, "rb") as f:
            f.seek(reverse_offset * -1, 2)
            rest_of_file = f.read()
            print(f.tell())
            with open(filename + ".mp4", "wb") as wf:
                wf.write(rest_of_file)
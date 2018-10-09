from PIL import Image, ImageFile
import glob
import argparse
import io

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pathname", type=str)
    parser.add_argument("--recursive", action="store_true")

    args = parser.parse_args()

    for filename in glob.iglob(args.pathname, recursive=args.recursive):
        print(filename)
        with open(filename, "rb") as f:
            #p = ImageFile.Parser()
            #while not p.finished:
            #    s = f.read(1024)
            #    if not s:
            #        break
            #    p.feed(s)
            img = Image.open(f)
            img.load()
            #hist = img.histogram()
            print(f.tell())
            print(len(img.tobytes()))
            endguess = f.tell()
            f.seek(0)
            allbytes = io.BytesIO(f.read(endguess))
            f.seek(0)
            originalbytes = io.BytesIO(f.read(endguess))

        laststableguess = endguess
        for current_increment in [10000, 1000, 100, 10, 1]:
            originalbytes.seek(0)
            allbytes = io.BytesIO(originalbytes.read())
            img = Image.open(allbytes)
            img.load()
            try:
                while endguess > 0:
                    endguess -= current_increment
                    allbytes.seek(0)
                    allbytes.truncate(endguess)
                    img = Image.open(allbytes)
                    img.load()
                    laststableguess = endguess
            except IOError as e:
                print("Got IOError at {}. {}".format(endguess, e))
                endguess = laststableguess
        print(endguess)

        with open(filename, "rb") as f:
            f.seek(endguess)
            rest_of_file = f.read()
            print(f.tell())
            with open(filename + ".mp4", "wb") as wf:
                wf.write(rest_of_file)
#!/usr/bin/env python3

# import userlib
import re
from pathlib import Path
from cli import Args


def main():

    # print("Nacitam knihovnu...")
    # print(dir(userlib))

    print("DEBUG: Args.args:", Args.args, '\n')

    # # Get user entered directories, ignore trailing slash
    # dirs = [d.strip('/') for d in Args.args.filenames]

    # First is Source directory, Other are destination directories
    src_dir = Args.args.source.strip('/')
    dst_dir = [d.strip('/') for d in Args.args.dest]

    print("DEBUG: src_dir:", src_dir)
    print("DEBUG: dst_dir:", dst_dir)

    # Get list of all directories in current folder
    curdir = Path('.')
    directories = sorted((d for d in curdir.iterdir() if d.is_dir()))

    # # Check if user-entered directories exists
    # for d in directories:
    #     res = any(d in dir_dst.append(dir_src) for d in directories)
    #     print('{}: {}'.format(d, res))


    # for directory in directories:


    # for idx, itempath in enumerate():
    #     itempath: Path
    #     print("DEBUG: itempath:", itempath.resolve())

        # if not re.match(r'.*_battery_.*.inc', str(itempath.resolve())):
        #     continue

        # if any([filename.strip('/') in str(itempath.resolve()) for filename in Args.args.filenames]):
        #     print(itempath.resolve())

        # # print("DEBUG: var:", var)
        # # if (re.match(r'.*_battery_.*.inc', str(itempath.resolve()))
        # #         and any(dirname in list(itempath.resolve()) for dirname in Args.args.filenames)):
        # #     print("DEBUG: itempath:", itempath)
        # if idx == 100:
        #     return


if __name__ == '__main__':
    main()

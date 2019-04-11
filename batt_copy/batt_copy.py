#!/usr/bin/env python3

# import userlib
import re
from pathlib import Path
from cli import Args


class Src:
    a4 = None
    bild = None
    defo = None
    battery_files = []


def main():

    # print("Nacitam knihovnu...")
    # print(dir(userlib))

    print("DEBUG: Args.args:", Args.args, '\n')

    # # Get user entered directories, ignore trailing slash
    # dirs = [d.strip('/') for d in Args.args.filenames]

    # First is Source directory, Other are destination directories
    curdir = Path('.')
    src_dir: Path = Path(curdir / Args.args.source.strip('/')).resolve()
    dst_dirs: Path = [Path(curdir / d.strip('/')).resolve() for d in Args.args.dest]

    print("DEBUG: src_dir:", src_dir)
    print("DEBUG: dst_dirs:", dst_dirs)

    # Get list of all directories in current folder
    directories = sorted((d for d in curdir.iterdir() if d.is_dir()))

    # # Check if user-entered directories exists
    # for d in directories:
    #     res = any(d in dir_dst.append(dir_src) for d in directories)
    #     print('{}: {}'.format(d, res))

    # Locate the src files
    # a4.ses, DFC_Lokale_Defo_pam, bild.ses, _battery_hv_, _battery_hv_modules_
    for itempath in src_dir.glob('**/*'):
        # Ignore files which are not in 'RESULTS' folder
        if itempath.parent.name != 'RESULTS':
            continue
        match = re.findall(r'_battery_hv_\d\d\d|_battery_hv_modules_\d\d\d', itempath.name)
        if match:
            Src.battery_files.append(itempath)
            print(itempath.resolve())

        elif itempath.name == 'a4.ses':
            Src.a4 = itempath
            print(itempath.resolve())
            print()
            with open(Src.a4, 'r') as f:
                lines = f.readlines()
            for line in lines:
                print(line, end='')
            print()

        elif itempath.name == 'DFC_Lokale_Defo_pam':
            Src.defo = itempath
            print(itempath.resolve())

        elif itempath.name == 'bild.ses':
            Src.bild = itempath
            print(itempath.resolve())

    print("Src.a4:", Src.a4)
    print("Src.bild:", Src.bild)
    print("Src.defo:", Src.defo)
    print("Src.battery_files:", Src.battery_files)

    # Files acquired, now copy them to 'destination directories'
    # for dst_dir in dst_dirs:
        # Check if the dir exists and RESULTS dir exists

        # Copy all files to the new RESULTS directory

        # Modify a4.ses - reflect new path
        # v[act]:wri png '.....'

        # Modify build.ses - reflect new ndame
        # rea geo Pamcrash './....'

        # Change dir to new RESULTS dir

        # Run ./DFC_Lokale_Defo_pam <...>.DSY.fz file_defo.DSY.fz <SK.._battery_hv_modules_..>.inc



if __name__ == '__main__':
    main()

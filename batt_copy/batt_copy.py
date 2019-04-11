#!/usr/bin/env python3

# import userlib
import re
from pathlib import Path
from cli import Args


class Src:
    def __init__(self):
        self.a4 = None
        self.bild = None
        self.defo = None
        self.battery_files = []

    @property
    def all_files(self):
        return [self.a4, self.bild, self.defo, self.battery_files]


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

    src_files = Src()
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
            src_files.battery_files.append(itempath)
            print(itempath.resolve())

        elif itempath.name == 'a4.ses':
            src_files.a4 = itempath
            print(itempath.resolve())

            # print()
            # with open(src_files.a4, 'r') as f:
            #     lines = f.readlines()
            # for line in lines:
            #     print(line, end='')
            # print()

        elif itempath.name == 'DFC_Lokale_Defo_pam':
            src_files.defo = itempath
            print(itempath.resolve())

        elif itempath.name == 'bild.ses':
            src_files.bild = itempath
            print(itempath.resolve())

    print("src_files.a4:", src_files.a4)
    print("src_files.bild:", src_files.bild)
    print("src_files.defo:", src_files.defo)
    print("src_files.battery_files:", src_files.battery_files)

    # Files acquired, now copy them to 'destination directories'
    for dst_dir in dst_dirs:
        dst_resuls_dir = dst_dir / 'RESULTS'

        # Check if the dir exists and RESULTS dir exists
        if not dst_resuls_dir.exists():
            print(f"ERROR: Destination directory not found: {dst_resuls_dir.resolve()}")
            continue

        print(f"\nAll files: {src_files.all_files}")

        # Copy all files to the new RESULTS directory

        # Modify a4.ses - reflect new path
        # v[act]:wri png '.....'

        # Modify build.ses - reflect new ndame
        # rea geo Pamcrash './....'

        # Change dir to new RESULTS dir

        # Run ./DFC_Lokale_Defo_pam <...>.DSY.fz file_defo.DSY.fz <SK.._battery_hv_modules_..>.inc



if __name__ == '__main__':
    main()

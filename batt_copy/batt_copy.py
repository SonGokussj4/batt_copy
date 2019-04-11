#!/usr/bin/env python3

# import userlib
import re
from pathlib import Path
from cli import Args
import shutil


class Files:
    def __init__(self, directory):
        self.directory = directory
        self.a4 = None
        self.bild = None
        self.defo = None
        self.battery_files = []
        self.find_files()

    def find_files(self):
        for itempath in self.directory.glob('**/*'):
            if itempath.parent.name != 'RESULTS':
                continue
            match = re.findall(r'_battery_hv_\d\d\d|_battery_hv_modules_\d\d\d', itempath.name)
            if match:
                self.battery_files.append(itempath)

            elif itempath.name == 'a4.ses':
                self.a4 = itempath

            elif itempath.name == 'DFC_Lokale_Defo_pam':
                self.defo = itempath

            elif itempath.name == 'bild.ses':
                self.bild = itempath

    @property
    def all_files(self):
        """Return all files."""
        files = [self.a4, self.bild, self.defo]
        files.extend(self.battery_files)
        return files


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

    src_files = Files(src_dir)
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

        # Copy all files to the new RESULTS directory
        print(f"\nAll files: {src_files.all_files}")
        for src_file in src_files.all_files:
            dst_file = dst_resuls_dir / src_file.name
            print(f"INFO: Copying {src_file.name} --> {dst_file.resolve()}")
            shutil.copyfile(src_file, dst_file)

        # Modify a4.ses - reflect new path
        # v[act]:wri png '.....'

        # Modify build.ses - reflect new ndame
        # rea geo Pamcrash './....'

        # Change dir to new RESULTS dir

        # Run ./DFC_Lokale_Defo_pam <...>.DSY.fz file_defo.DSY.fz <SK.._battery_hv_modules_..>.inc



if __name__ == '__main__':
    main()

#!/usr/bin/env python3

# import userlib
import re
import shutil
import myclass
from cli import Args
from pathlib import Path


# TODO:
# a4, bild a DFC to kopiruje z SOURCE_FILES
# /ST/Evektor/UZIV/JVERNER/PROJEKTY/GIT/jverner/batt_copy/batt_copy/source_files
#
# start
# v puvodnim to kopiruje battery z MODEL (vzdy)
# pak se to podiva, zda je ta fyzicky udelana baterie
# pokud neni, tak to automaticky pres ansu vytvori
#   otevre, nacte to puvodni baterii
#   vyfiltruje to, co je potreba a ulozi pod includem
#   doda se lepsi jmeno
# pokud je, ta se to uzivate zepta (automatika?), zda ji chce kopirovat nebo vytvorit
# pak to ze SOURCE_FILES zkopiruje
# a4.ses
#   v nem nahradi v radku: v[act]:wri png 'DST_RESULTS_FOLDER/BATTERY_DEFORMACE.png'
#   DST_RESULTS_FOLDER za RESULTS slozku targetu
# bild.ses
#   v nem nahradi v radku: rea geo Pamcrash './MODEL_BATTERY_INC'
#   MODEL_BATTERY_INC za nazev .inc te baterie prekpirovane z modelu
# DFC_Lokale_Defo_pam
#
# V cilove slozce to najde vsechny DSY.fz soubory, mel by byt jen jeden
#
# Jakmile je zkopirovano, tak se tam skript CD
# a spusti
# ./DFC_Lokale_Defo_pam <nalezeny.DSY.fz> file_defo.DSY.fz <upraveny_SK..._battery_hv_modules_...inc>
# konec



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

    # Find battery files from Source Dir
    # from MODEL folder - base battery include
    # from RESULTS folder - edited battery include, if it's there, ask if create or copy
    batt_files = myclass.BattFiles(src_dir)
    print("BASE_BATT: ", batt_files.base_batt.name)
    print("MODIF_BATT: ", batt_files.modif_batt.name)

    # Copy base batt into dest folder


    exit()


    src_files = myclass.Files(src_dir)
    # print("src_files.a4:", src_files.a4)
    # print("src_files.bild:", src_files.bild)
    # print("src_files.defo:", src_files.defo)
    # print("src_files.battery_files:", src_files.battery_files)

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
            # shutil.copyfile(src_file, dst_file)

        dst_files = myclass.Files(dst_dir)
        # print("dst_files.a4:", dst_files.a4)
        # print("dst_files.bild:", dst_files.bild)
        # print("dst_files.defo:", dst_files.defo)
        # print("dst_files.battery_files:", dst_files.battery_files)

        # Modify a4.ses - reflect new path
        # v[act]:wri png '.....'
        dst_files.modify_a4()

        # Modify build.ses - reflect new ndame
        # rea geo Pamcrash './....'
        dst_files.modify_bild()

        # Change dir to new RESULTS dir

        # Run ./DFC_Lokale_Defo_pam <...>.DSY.fz file_defo.DSY.fz <SK.._battery_hv_modules_..>.inc



if __name__ == '__main__':
    main()


# from tempfile import mkstemp
# from shutil import move
# from os import remove

# def replace(source_file_path, pattern, substring):
#     fh, target_file_path = mkstemp()
#     with open(target_file_path, 'w') as target_file:
#         with open(source_file_path, 'r') as source_file:
#             for line in source_file:
#                 target_file.write(line.replace(pattern, substring))
#     remove(source_file_path)
#     move(target_file_path, source_file_path)

#!/usr/bin/env python3

import os
import re
import shutil
import myclass
from cli import Args
from pathlib import Path
from pycolor import atr, fg, bg  # atr.b, atr.reset_all, fg.lr, fg.g

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

    # First is Source directory, Other are destination directories
    curdir = Path('.')
    src_dir: Path = Path(curdir / Args.args.source.strip('/')).resolve()
    dst_dirs: Path = [Path(curdir / d.strip('/')).resolve() for d in Args.args.dest]

    # Find battery files from Source Dir
    # from MODEL folder - base battery include
    # from RESULTS folder - edited battery include, if it's there, ask if create or copy
    batt_files = myclass.BattFiles(src_dir)

    # Files acquired, now copy them to 'destination directories'
    for dst_dir in dst_dirs:
        dst_resuls_dir = dst_dir / 'RESULTS'

        # Check if the dest RESULTS dir exists
        if not dst_resuls_dir.exists():
            print(f"{atr.bo}{fg.lr}[ WARNING ]{atr.reset_all} Destination directory not found: {dst_resuls_dir.resolve()}")
            continue

        # Copy base batt into dest folder
        batt_files.copy_base_batt(dst_resuls_dir)

        # Check if modif batt exists, if not, create it from the base one
        if batt_files.modif_batt is not None:
            print(f"{atr.bo}[ INFO ]{atr.reset_all} Modif batt exists, copying...")
            batt_files.copy_modif_batt(dst_resuls_dir)
        else:
            modif_batt_name = batt_files.base_batt.name.replace('battery_hv', 'battery_hv_modules')
            batt_files.modif_batt = dst_resuls_dir / modif_batt_name
            if batt_files.modif_batt.exists():
                res = input(f"{atr.bo}{fg.y}[ WARNING ]{atr.reset_all} Modif batt found in target directory. Create anyway? [yN]: ")
                if res.lower() in ['y', 'yes']:
                    batt_files.create_modif_batt()
                else:
                    print(f"{atr.bo}[ INFO ]{atr.reset_all} Modified battery was not created")
            else:
                res = input(f"{atr.bo}{fg.y}[ WARNING ]{atr.reset_all} Modif batt not found. Create? [yN]: ")
                if res.lower() in ['y', 'yes']:
                    batt_files.create_modif_batt()
                if batt_files.modif_batt.exists():
                    print(f"{atr.bo}[ INFO ]{atr.reset_all} Modified battery created.")
                else:
                    print(f"{atr.bo}{fg.lr}[ WARNING ]{atr.reset_all} Something went wrong within ANSA script. Modified battery was not created.")

    src_files = myclass.SourceFiles()
    # Copy and modify source files (a4.ses, bild.ses, DFC_Lokale_Defo_pam)
    src_files.copy_modif_a4(dst_resuls_dir)
    src_files.copy_modif_bild(dst_resuls_dir, inc_name=batt_files.base_batt.name)
    src_files.copy_DFC(dst_resuls_dir)

    # Change dir to new RESULTS dir
    os.chdir(dst_resuls_dir)

    # Get the DSY.fz file
    for itempath in dst_resuls_dir.glob('*.DSY.fz'):
        if itempath.name.endswith('DSY.fz') and itempath.name.startswith('SK'):
            dsy_file = itempath
            print(f"{atr.bo}[ INFO ]{atr.reset_all} DSY file found... '{dsy_file.resolve()}'")
            continue

    cmd = f'./DFC_Lokale_Defo_pam {dsy_file.name} file_defo.DSY.fz {batt_files.modif_batt.name}'
    print(f"{atr.bo}[ INFO ]{atr.reset_all} Running cmd: '{cmd}'")
    os.system(cmd)


if __name__ == '__main__':
    main()

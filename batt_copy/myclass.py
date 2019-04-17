"""
Class that contains helper Classes.

SourceFiles
    self.a4
    self.bild
    self.DFC

Files
"""
import re
import os
import shutil
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
SOURCE_FILES = SCRIPT_DIR / 'source_files'


class SourceFiles:
    def __init__(self):
        self._directory = SOURCE_FILES
        self.a4 = self._directory / 'a4.ses'
        self.bild = self._directory / 'bild.ses'
        self.DFC = self._directory / 'DFC_Lokale_Defo_pam'

    def copy_modif_a4(self, dst_dir):
        """
        Modify a4.ses - reflect new path

        v[act]:wri png 'DST_RESULTS_FOLDER/BATTERY_DEFORMACE.png'
        """
        dst_filepath = dst_dir / 'a4.ses'
        print(f"[ INFO ] Copying a4.ses --> {dst_filepath}")
        shutil.copyfile(self.a4, dst_filepath)

        print(f"[ INFO ] Modifying: {dst_filepath}")
        with open(dst_filepath, 'r') as f:
            lines = f.readlines()
        lines = [re.sub(r"DST_RESULTS_FOLDER", str(dst_dir.resolve()), line)
                 if line.startswith("v[act]:wri png 'DST_RESULTS_FOLDER")
                 else line
                 for line in lines]
        with open(dst_filepath, 'w') as f:
            f.writelines(lines)
            print(f"[ INFO ] Lines within {dst_filepath.name} updated")

    def copy_modif_bild(self, dst_dir, inc_name):
        """
        Modify bild.ses - reflect new include name

        rea geo Pamcrash './MODEL_BATTERY_INC'
        """
        dst_filepath = dst_dir / 'bild.ses'
        print(f"[ INFO ] Copying bild.ses --> {dst_filepath}")
        shutil.copyfile(self.bild, dst_filepath)

        print(f"[ INFO ] Modifying: {dst_filepath}")
        with open(dst_filepath, 'r') as f:
            lines = f.readlines()

        lines = [re.sub(r"MODEL_BATTERY_INC", inc_name, line)
                 if line.startswith("rea geo Pamcrash './MODEL_BATTERY_INC'")
                 else line
                 for line in lines]
        with open(dst_filepath, 'w') as f:
            f.writelines(lines)
            print(f"[ INFO ] Lines within {dst_filepath.name} updated")

    def copy_DFC(self, dst_dir):
        """Copy DFC_Lokale_Defo_pam file into dst_dir."""
        dst_filepath = dst_dir / self.DFC.name
        print(f"[ INFO ] Copying {self.DFC.name} --> {dst_filepath}")
        shutil.copyfile(self.DFC, dst_filepath)


class BattFiles:
    """
    Find battery files from Source Dir
        from MODEL folder - base battery include
        from RESULTS folder - edited battery include, if it's there, ask if create or copy
    """

    def __init__(self, directory):
        self._directory = directory
        self.base_batt = self._get_base_batt()
        self.modif_batt = self._get_modif_batt()

    def _get_base_batt(self):
        """Search through SRC MODEL folder and return inc .*_batter_hv_NumNumNum.*"""
        # TODO: jestlize nebude nalezena v MODEL, tak hledat v RESULTS?
        MODEL_dir = self._directory / 'MODEL'
        found_batteries = []
        for itempath in MODEL_dir.glob('*.inc'):
            match = re.findall(r'_battery_hv_\d\d\d', itempath.name)
            if match:
                found_batteries.append(itempath)
        if len(found_batteries) > 1:
            print("[ WARNING ] Found more batteries... WHAT NOW??? EXIT")
            exit()
        return found_batteries[0]

    def _get_modif_batt(self):
        """Search through SRC RESULTS folder and return inc .*_batter_hv_modules_NumNumNum.*"""
        RESULTS_dir = self._directory / 'RESULTS'
        found_batteries = []
        for itempath in RESULTS_dir.glob('*.inc'):
            match = re.findall(r'_battery_hv_modulses_\d\d\d', itempath.name)
            if match:
                found_batteries.append(itempath)
        if len(found_batteries) > 1:
            print("[ WARNING ] Found more MODIFIED batteries... WHAT NOW??? EXIT")
            exit()
        elif len(found_batteries) == 0:
            print("[ INFO ] _batter_hv_modules_ include not found. Creating...")
            # TODO: Ansa script to create a battery
            return None
        return found_batteries[0]

    def copy_base_batt(self, target):
        """Copy SRC battery into target folder."""
        # TODO: nekopirovat to i do MODEL folder?
        target_filepath = target / self.base_batt.name
        print(f"[ INFO ] Copying {self.base_batt} --> {target_filepath}")
        os.system("rsync -ah --progress {} {}".format(self.base_batt, target_filepath))
        # shutil.copy(self.base_batt, target_filepath)
        print(f"[ INFO ] Base battery copied.")

    def copy_modif_batt(self, target):
        """Copy MODIF battery into target folder."""
        target_filepath = target / self.modif_batt.name
        print(f"[ INFO ] Copying {self.modif_batt} --> {target_filepath}")
        os.system("rsync -ah --progress {} {}".format(self.modif_batt, target_filepath))
        # shutil.copy(self.modif_batt, target_filepath)
        print(f"[ INFO ] MODIF battery copied.")

    def create_modif_batt(self):
        """Start Ansa in background and create a Modified battery form Base battery."""
        print("[ INFO ] Creating modif battery...")
        script_path = '{parent_folder}/modifybatt.py'.format(parent_folder=Path(__file__).parent)
        os.system('/expSW/SOFTWARE/BETA_CAE_Systems/ansa_v19.1.1/ansa64.sh '
                  '-b '  # background
                  '-lm_retry 5 '  # if no licence, try again in 5 second
                  '-exec "load_script:{script_path}" '  # start this script
                  '-exec "main(\'{base_batt}\', \'{modif_batt}\')"'.format(  # and function main(args, ...)
                      script_path=script_path, base_batt=self.base_batt, modif_batt=self.modif_batt))

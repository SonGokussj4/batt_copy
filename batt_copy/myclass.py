"""
Class that contains helper Classes.

SourceFiles
    self.a4
    self.bild
    self.DFC

Files
"""
import re
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
SOURCE_FILES = SCRIPT_DIR / 'source_files'


class SourceFiles:
    def __init__(self):
        self._directory = SOURCE_FILES
        self.a4 = self._directory / 'a4.ses'
        self.bild = self._directory / 'bild.ses'
        self.DFC = self._directory / 'DFC_Lokale_Defo_pam'


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
        MODEL_dir = self._directory / 'MODEL'
        found_batteries = []
        for itempath in MODEL_dir.glob('*.inc'):
            match = re.findall(r'_battery_hv_\d\d\d', itempath.name)
            if match:
                found_batteries.append(itempath)
        if len(found_batteries) > 1:
            print("WARNING: Found more batteries... WHAT NOW??? EXIT")
            exit()
        return found_batteries[0]

    def _get_modif_batt(self):
        r"""Search through SRC RESULTS folder and return inc .*_batter_hv_modules_\d\d\d.*"""
        RESULTS_dir = self._directory / 'RESULTS'
        found_batteries = []
        for itempath in RESULTS_dir.glob('*.inc'):
            match = re.findall(r'_battery_hv_modules_\d\d\d', itempath.name)
            if match:
                found_batteries.append(itempath)
        if len(found_batteries) > 1:
            print("WARNING: Found more MODIFIED batteries... WHAT NOW??? EXIT")
            exit()
        elif len(found_batteries) == 0:
            print("_batter_hv_modules_ include not found. Creating...")
            # TODO: Ansa script to create a battery
            return 0
        return found_batteries[0]


class Files:
    """Input: project directory, eg. SK3165EUB_ABF_103."""

    def __init__(self, directory):
        self.directory = directory
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

    def modify_a4(self):
        """
        Modify a4.ses - reflect new path

        v[act]:wri png '.....'
        """
        print(f"Modifying: {self.a4.name}")
        with open(self.a4, 'r') as f:
            lines = [line.strip() for line in f.readlines()]
        lines = [re.sub(r"/ST/.*/RESULTS", str(self.a4.parent.resolve()), line)
                 if line.startswith('v[act]:wri png')
                 else line
                 for line in lines]
        with open(self.a4, 'w') as f:
            f.writelines(lines)
            print(f"Lines within {self.a4.name} updated")

    def modify_bild(self):
        """
        Modify build.ses - reflect new ndame

        # rea geo Pamcrash './....'
        """
        print(f"Modifying: {self.bild.name}")
        with open(self.bild, 'r') as f:
            lines = [line.strip() for line in f.readlines()]

        # newlines = []
        # for line in lines:
        #     if line.startswith("rea geo Pamcrash './SK") and '_battery_' in line:
        #         newline = re.sub(r"/ST/.*/RESULTS", str(self.a4.parent.resolve()), line)
        #         newlines.append(f'{newline}\n')
        #     else:
        #         newlines.append(f'{line}\n')
        # with open(self.bild, 'w') as f:
        #     f.writelines(newlines)
        #     print(f"Lines within {self.bild.name} updated")

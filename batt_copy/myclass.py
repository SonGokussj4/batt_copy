"""
Class that contains helper Classes.

SourceFiles
    self.a4
    self.bild
    self.DFC

Files
"""
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
SOURCE_FILES = SCRIPT_DIR / 'source_files'


class SourceFiles:
    def __init__(self):
        self._directory = SOURCE_FILES
        self.a4 = self._directory / 'a4.ses'
        self.bild = self._directory / 'bild.ses'
        self.DFC = self._directory / 'DFC_Lokale_Defo_pam'

#!/usr/bin/env python3

import sys
from os import chdir
from os.path import dirname
from time import sleep
from typing import NoReturn

import PyLoadBar

sys.path.insert(0, dirname(dirname(__file__))) # Ensure main module can be found by Python.
chdir(dirname(__file__))

import VBPatcher.globalvars.globalvars
from VBPatcher.applogger.applogger import logger
from VBPatcher.downloader.downloader import _Downloader
from VBPatcher.patching.patching import _Patcher
from VBPatcher.subprocessing.subprocessing import _exitPatcher, _openValheim
from VBPatcher.validation.validation import _Validate

__version__: str = '0.6.0'


DL = _Downloader()
Patcher = _Patcher()
Validations = _Validate()
bar = PyLoadBar.PyLoadBar()

#$ ====================================================================================================== $#

def main() -> None | NoReturn:
    """Program entry point.

    ---

    :return: start VBPatcher.
    :rtype: None | NoReturn
    """
    logger.info(f'Welcome to the Valheim Bepinex Patcher v{__version__}!\n>> Session Start: {VBPatcher.globalvars.globalvars._datefmt}\n\n')

    Validations._start_checks() # Ensure presence of patch files.

    while True:
        logger.info('Display user menu...')
        choosePatch: str = input(
            f"Welcome to the Valheim Bepinex Patcher!\n\nPlease Choose an Option by Entering its Corresponding Number:\n\n{VBPatcher.globalvars.globalvars._textborder}\n>> [1] Patch BepInEx to latest stable release: {VBPatcher.globalvars.globalvars.b_stable} (2/3/22)\n>> [2] Patch BepInEx to latest development/expiremental build: {VBPatcher.globalvars.globalvars.b_dev} (5/7/22)\n>> [3] Apply both patches to BepInEx in chronological order of release ({VBPatcher.globalvars.globalvars.b_stable} then {VBPatcher.globalvars.globalvars.b_dev})\n>> [4] Check for/update to newest patch versions\n>> [5] Open Valheim\n>> [6] Exit Program\n\n> "
        )
        match choosePatch:
            case '1': Patcher._patch_stable()
            case '2': Patcher._patch_dev()
            case '3': Patcher._patch_full()
            case '4':
                DL._UpdatePatcher()
                continue
            case '5': _openValheim()
            case '6':
                logger.info('BepInEx patching process cancelled...\n>> Preparing to exit...\n')
                bar.load('\nBepInEx patching process cancelled', 'Preparing to exit...', enable_display=False)
                return _exitPatcher()
            case _:
                logger.warning(f'Invalid Input:\n>> "{choosePatch}"\n\n>> Must ONLY enter:\n>> [1] for stable release {VBPatcher.globalvars.globalvars.b_stable}\n>> [2] for development build {VBPatcher.globalvars.globalvars.b_dev}\n>> [3] for FULL upgrade (apply both patches in order of release)\n>> [4] to update available patch versions/builds\n>> [5] to open Valheim\n>> [6] to exit program\n')
                print(f'\nERROR: Invalid Input -\n\n>> Your Entry:  "{choosePatch}".\n\n>> Must ONLY enter:\n>> [1] for stable release {VBPatcher.globalvars.globalvars.b_stable}\n>> [2] for development build {VBPatcher.globalvars.globalvars.b_dev}\n>> [3] for FULL upgrade (apply both patches in order of release)\n>> [4] to update available patch versions/builds\n>> [5] to open Valheim\n>> [6] to exit program\n\n')
                sleep(1.5)
                continue

        return _exitPatcher()

if __name__ == '__main__':
    main()

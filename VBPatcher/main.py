#!/usr/bin/env python3

import sys
from os import chdir
from os.path import dirname
from time import sleep

from PyLoadBar import PyLoadBar

sys.path.insert(0, dirname(
    dirname(__file__)))  # Ensure main module can be found by Python.
chdir(dirname(__file__))  # Change cwd to main module directory.

import VBPatcher.appglobals.globals
from VBPatcher.apploggers.loggers import logger, logger_stream
from VBPatcher.downloader.downloader import _Downloader
from VBPatcher.patching.patching import _Patcher
from VBPatcher.subprocessing.subprocessing import _exitPatcher, _openValheim
from VBPatcher.validation.validation import _Validate

DL = _Downloader()  # Initialize Downloader.
Patcher = _Patcher()  # Initialize Patcher.
Validations = _Validate()  # Initialize Validations.
cancel = PyLoadBar(False)  # Initialize text-based loading sequence.

#$ ====================================================================================================== $#


def main() -> None:
    """Program entry point.

    ---

    :return: start VBPatcher.
    :rtype: `None`
    """

    logger.info(
        f'Welcome to the Valheim Bepinex Patcher v{VBPatcher.appglobals.globals.__version__}!\n>> Session Start: {VBPatcher.appglobals.globals.datefmt}\n\n'
    )

    Validations._start_checks()  # Ensure presence of patch files.

    return display_menu()


def display_menu() -> None:
    """Display patcher menu.

    ---

    :return: chosen patcher process.
    :rtype: `None`
    """

    while True:
        logger.info('Display user menu...\n')
        choosePatch: str = input(
            f"Welcome to the Valheim Bepinex Patcher v{VBPatcher.appglobals.globals.__version__}!\n\nPlease Choose an Option by Entering its Corresponding Number:\n\n{VBPatcher.appglobals.globals.textborder}\n>> [1] Patch BepInEx to latest stable release: {VBPatcher.appglobals.globals.b_stable}\n>> [2] Patch BepInEx to latest development/bleeding-edge build: {VBPatcher.appglobals.globals.b_dev}\n>> [3] Apply both patches to BepInEx in chronological order of release ({VBPatcher.appglobals.globals.b_stable} then {VBPatcher.appglobals.globals.b_dev})\n>> [4] Check for/update to newest patch versions\n>> [5] Open Valheim\n>> [6] Exit Program\n\n> "
        )

        if choosePatch == '1':  # Patch BepInEx to latest stable release.
            logger.info(
                'Chose option [1] to patch BepInEx to latest stable release...'
            )
            Patcher._patch_stable()

        elif choosePatch == '2':  # Patch BepInEx to latest development/bleeding-edge build.
            logger.info(
                'Chose option [2] to patch BepInEx to latest dev-build...')
            Patcher._patch_dev()

        elif choosePatch == '3':  # Apply both patches to BepInEx in chronological order of release.
            logger.info(
                'Chose option [3] to install both stable and development patch builds in order of release...'
            )
            Patcher._patch_full()

        elif choosePatch == '4':  # Check for/update to newest patch versions.
            logger.info('Chose option [4] to check for new patch updates...')
            DL.UpdatePatcher()

        elif choosePatch == '5':  # Open Valheim.
            logger.info('Chose option [5] to start Valheim...')
            _openValheim()

        elif choosePatch == '6':  # Exit Program.
            logger.info('Chose option [6] to close patcher...')
            logger.info(
                'Completed VBPatcher processes...\n>> Preparing to exit...\n')

            cancel.start('Completed VBPatcher processes',
                         'Exiting...',
                         iter_total=5,
                         txt_iter_speed=0.25)

            return _exitPatcher()

        else:  # Invalid input.
            logger_stream.warning(
                f'ERROR - Invalid Input\n\n>> Your Entry: "{choosePatch}".\n\n>> Must ONLY enter:\n>> [1] for stable release {VBPatcher.appglobals.globals.b_stable}\n>> [2] for development build {VBPatcher.appglobals.globals.b_dev}\n>> [3] for FULL upgrade (apply both patches in order of release)\n>> [4] to update available patch versions/builds\n>> [5] to open Valheim\n>> [6] to exit program\n\n'
            )
            sleep(1.5)


if __name__ == '__main__':
    main()

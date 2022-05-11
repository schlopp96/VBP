#!/usr/bin/env python3

import msvcrt as m
import os
from globals import *
from downloader.downloader import _Downloader
from os import PathLike, chdir, unlink
from os.path import dirname
from shutil import copytree
from subprocess import TimeoutExpired, call
from sys import exit as ex
from time import sleep
from typing import NoReturn
import applogger.applogger
from PyLoadBar import load

chdir(dirname(__file__))



#@ Declare global variables containing file locations and patch-install destinations:



__version__: str = '0.6.0'


#$ ====================================================================================================== $#

logger = applogger.applogger._LogGenerator(globals._logFile)


DL = _Downloader()


def _start_checks() -> None:
    """Verify application has latest BepInEx patches upon start.

    :return: continue to application if verification is successful, otherwise exits program.
    :rtype: None
    """
    logger.info('Checking for application BepInEx patch files...\n')

    if _verify_stable(globals.url_stable) and _verify_dev(globals.url_dev):
        logger.info('Successfully verified BepInEx patch files!\n')
    else:
        logger.info('One or more patch files were not able to be verified...')
        load('ERROR: One or more patch files were not able to be verified', 'Exiting Patcher', enable_display=False)
        return _exitPatcher()


def VBPatcher() -> None | NoReturn:
    """Program entry point.

    ---

    :return: start VBPatcher.
    :rtype: None | NoReturn
    """
    logger.info(f'Welcome to the Valheim Bepinex Patcher v{__version__}!\n>> Session Start: {globals._datefmt}\n\n')

    _start_checks() # Ensure presence of patch files.

    while True:
        logger.info('Display user menu...')
        choosePatch: str = input(
            f"Welcome to the Valheim Bepinex Patcher!\n\nPlease Choose an Option by Entering its Corresponding Number:\n\n{globals._textborder}\n>> [1] Patch BepInEx to latest stable release: {globals.b_stable} (2/3/22)\n>> [2] Patch BepInEx to latest development/expiremental build: {globals.b_dev} (5/7/22)\n>> [3] Apply both patches to BepInEx in chronological order of release ({globals.b_stable} then {globals.b_dev})\n>> [4] Check for/update to newest patch versions\n>> [5] Open Valheim\n>> [6] Exit Program\n\n> "
        )
        match choosePatch:
            case '1': _patch_stable()
            case '2': _patch_dev()
            case '3': _patch_full()
            case '4':
                _UpdatePatcher()
                continue
            case '5': _openValheim()
            case '6':
                logger.info('BepInEx patching process cancelled...\n>> Preparing to exit...\n')
                load('\nBepInEx patching process cancelled', 'Preparing to exit...', enable_display=False)
                return _exitPatcher()
            case _:
                logger.warning(f'Invalid Input:\n>> "{choosePatch}"\n\n>> Must ONLY enter:\n>> [1] for stable release {globals.globals.b_stable}\n>> [2] for development build {globals.globals.b_dev}\n>> [3] for FULL upgrade (apply both patches in order of release)\n>> [4] to update available patch versions/builds\n>> [5] to open Valheim\n>> [6] to exit program\n')
                print(f'\nERROR: Invalid Input -\n\n>> Your Entry:  "{choosePatch}".\n\n>> Must ONLY enter:\n>> [1] for stable release {globals.globals.b_stable}\n>> [2] for development build {globals.b_dev}\n>> [3] for FULL upgrade (apply both patches in order of release)\n>> [4] to update available patch versions/builds\n>> [5] to open Valheim\n>> [6] to exit program\n\n')
                sleep(1.5)
                continue

        return _exitPatcher()


def _verify_stable(url):
    """Validate presence of BepInEx stable release patch files.

    :param url: url to download BepInEx stable release from if not found.
    :type url: Any
    :return: validation of patch files.
    :rtype: bool
    """
    logger.info(f'Validating stable-build {globals.globals.b_stable} patch files...\n')

    stable_files: list = [['.gitkeep', 'changelog.txt', 'winhttp.dll'], [], ['BepInEx/core/0Harmony.dll', 'BepInEx/core/0Harmony.xml', 'BepInEx/core/0Harmony20.dll', 'BepInEx/core/BepInEx.dll', 'BepInEx/core/BepInEx.Harmony.dll', 'BepInEx/core/BepInEx.Harmony.xml', 'BepInEx/core/BepInEx.Preloader.dll', 'BepInEx/core/BepInEx.Preloader.xml', 'BepInEx/core/BepInEx.xml', 'BepInEx/core/HarmonyXInterop.dll', 'BepInEx/core/Mono.Cecil.dll', 'BepInEx/core/Mono.Cecil.Mdb.dll', 'BepInEx/core/Mono.Cecil.Pdb.dll', 'BepInEx/core/Mono.Cecil.Rocks.dll', 'BepInEx/core/MonoMod.RuntimeDetour.dll', 'BepInEx/core/MonoMod.RuntimeDetour.xml', 'BepInEx/core/MonoMod.Utils.dll', 'BepInEx/core/MonoMod.Utils.xml']]

    stable_match: bool = False

    found = []

    try:
        found.extend(file for (root, dirs, file) in os.walk('./patch-files/stable', topdown=True))

        if found.sort() == stable_files.sort():
            stable_match = True
            logger.info(f'Stable-build {globals.globals.b_stable} patch files verified successfully!\n')

        else:
            logger.info(f'Unable to verify stable patch {globals.globals.b_stable} files...\n>> Attempting to download...\n')
            DL.dl_stable(url)
            DL._unzip_patch(f'./patch-files/stable/BepInEx_stable_{globals.globals.b_stable}.zip', True)
            stable_match = True
            logger.info(f'Successfully downloaded stable-build {globals.globals.b_stable} patch files!\n')
        return stable_match

    except Exception as err:
        stable_match = False
        logger.error(f'Encountered error during application start checks...\n>> Exception: {err}\n')

    finally:
        return stable_match


def _verify_dev(url):
    """Validate presence of BepInEx development build patch files.

    :param url: url to download BepInEx development build from if not found.
    :type url: PathLike | str
    :return: validation of patch files.
    :rtype: bool
    """
    logger.info(f'Validating development patch {globals.b_dev} files...\n')

    dev_files: list = [['.gitkeep', 'changelog.txt', 'winhttp.dll'], [], ['BepInEx/core/MonoMod.RuntimeDetour.dll', 'BepInEx/core/BepInEx.Core.xml', 'BepInEx/core/MonoMod.Utils.dll', 'BepInEx/core/0Harmony.dll', 'BepInEx/core/BepInEx.Unity.dll', 'BepInEx/core/Mono.Cecil.Pdb.dll', 'BepInEx/core/BepInEx.Preloader.Unity.dll', 'BepInEx/core/BepInEx.Preloader.Core.xml', 'BepInEx/core/Mono.Cecil.Mdb.dll', 'BepInEx/core/Mono.Cecil.dll', 'BepInEx/core/Mono.Cecil.Rocks.dll', 'BepInEx/core/SemanticVersioning.dll', 'BepInEx/core/BepInEx.Core.dll', 'BepInEx/core/BepInEx.Preloader.Unity.xml', 'BepInEx/core/BepInEx.Unity.xml', 'BepInEx/core/BepInEx.Preloader.Core.dll']]

    dev_match: bool = False

    found = []

    try:
        found.extend(file for (root, dirs, file) in os.walk('./patch-files/development/', topdown=True))
        if found.sort() == dev_files.sort():
            dev_match = True
            logger.info(f'Development patch {globals.b_dev} files verified successfully!\n')

        else:
            logger.info(f'Unable to verify development patch {globals.b_dev} files...\n>> Attempting to download...\n')
            DL.dl_dev(url)
            DL._unzip_patch(f'./patch-files/development/BepInEx_dev_{globals.b_dev}.zip', False)
            dev_match = True
            logger.info(f'Successfully downloaded development patch {globals.b_dev} files!\n')
        return dev_match

    except Exception as err:
        dev_match = False
        logger.error(f'Encountered error during application start checks...\n>> Exception: {err}\n')

    finally:
        return dev_match


def _patch_stable() -> None | NoReturn:
    """Install latest BepInEx stable-build release version to local directory.

    ---

    :return: patched BepInEx installation.
    :rtype: None
    """
    while True:
        logger.info(f'Prompting user for installation of BepInEx stable release {globals.b_dev} patch...')
        confirmStable: str = input(
            f'\nReally patch BepInEx to latest stable-release {globals.b_stable} in location:\n\n>> "{globals.p_targetDir}"?\n\n> Enter [y] or [n]:\n{globals._textborder}\n> '
        )
        match confirmStable.lower():
            case 'yes'|'y':
                _patch(globals.p_stable, globals.p_targetDir, globals.b_stable)
                _startPrompt()
            case 'n'|'no':
                logger.info('BepInEx patching process cancelled...\n>> Preparing to exit...\n')
                load('\nBepInEx patching process cancelled', 'Preparing to exit...', enable_display=False)
                return _exitPatcher()
            case _:
                logger.warning(f'Invalid Input: "{confirmStable}"\n>> Must ONLY enter either [y] for "YES" or [n] for "NO".\n')
                print(f'\nERROR: Invalid Input\n\n>> Your Entry: "{confirmStable}".\n\n>> Must ONLY enter either [y] for "YES" or [n] for "NO".\n\n')
                sleep(1.250)
                continue


def _patch_dev() -> None | NoReturn:
    """Install latest BepInEx development patch version to local directory.

    ---

    :return: patched BepInEx installation.
    :rtype: None
    """
    while True:
        logger.info(f'Prompting user for installation of BepInEx development build {globals.b_dev} patch...')
        confirmLatest: str = input(
            f'\nReally patch BepInEx to latest development build {globals.b_dev} in location:\n\n>> "{globals.p_targetDir}"?\n\n> Enter [y] or [n]:\n{globals._textborder}\n> '
        )
        match confirmLatest.lower():
            case 'yes'|'y':
                _patch(globals.p_dev, globals.p_targetDir, globals.b_dev)
                _startPrompt()
            case 'n'|'no':
                logger.info('BepInEx patching process cancelled...\n>> Preparing to exit...\n')
                load('\nBepInEx patching process cancelled', 'Preparing to exit...', enable_display=False)
                return _exitPatcher()
            case _:
                logger.warning(f'Invalid Input: "{confirmLatest}"\n>> Must ONLY enter either [y] for "YES" or [n] for "NO".\n')
                print(f'\nERROR: Invalid Input\n\n>> Your Entry: "{confirmLatest}".\n\n>> Must ONLY enter either [y] for "YES" or [n] for "NO".\n\n')
                sleep(1.250)
                continue


def _patch_full() -> None | bool:
    """Apply both available BepInEx patches in order of release (Stable -> Development).

    ---

    :return: patched BepInEx installation.
    :rtype: None
    """
    while True:
        logger.info('Displaying confirmation prompt to install full-upgrade patch (install both stable and development builds in order of release)...')
        confirmFull: str = input(
            f'\nReally apply both latest stable release {globals.b_stable}, and latest development build {globals.b_dev}?\n> Enter [y] or [n]:\n{globals._textborder}\n> '
        )
        match confirmFull.lower():
            case 'yes'|'y':
                _patch(globals.globals.p_stable, globals.globals.p_targetDir, globals.globals.b_stable)
                _patch(globals.p_dev, globals.globals.p_targetDir, globals.b_dev)
                return _startPrompt()
            case 'n'|'no':
                logger.info('BepInEx patching process cancelled...\n>> Preparing to exit...\n')
                load('\n>> BepInEx patching process cancelled', '>> Preparing to exit...', enable_display=False)
                return _exitPatcher()
            case _:
                logger.warning(f'Invalid Input: "{confirmFull}"\n>> Must ONLY enter either [y] for "YES" or [n] for "NO".\n')
                print(f'\nERROR: Invalid Input\n\n>> Your Entry: "{confirmFull}".\n\n>> Must ONLY enter either [y] for "YES" or [n] for "NO".\n\n')
                sleep(1.250)
                continue


def _startPrompt() -> NoReturn | None:
    """Prompt user to decide whether to start Valheim immediately after program exit or not.

    ---

    :return: display user prompt.
    :rtype: NoReturn | None
    """
    while True:
        logger.info('Displaying start game prompt...')
        startPrompt: str = input(
            f'\nStart Game?\n\n> Enter [y] or [n]:\n{globals._textborder}\n> ')
        match startPrompt.lower():
            case 'y'|'yes':
                _openValheim()
                return _exitPatcher()
            case 'n'|'no':
                logger.info('Patching process successfully completed!\n>> Preparing to exit...\n')
                load('\nPatching process successfully completed',
                     '\nPreparing to exit...', enable_display=False)
                return _exitPatcher()
            case _:
                logger.warning(f'Invalid Input: "{startPrompt}"\n>> Must ONLY enter either [y] for "YES" or [n] for "NO".\n')
                print(f'\nERROR: Invalid Input\n\n>> Your Entry: "{startPrompt}".\n\n>> Must ONLY enter either [y] for "YES" or [n] for "NO".\n\n')
                sleep(1.250)
                continue


def _openValheim() -> int | None:
    """Calls command to open "Valheim" within Steam client.
    - Will raise `TimeoutExpired` exception if executable doesn't start within 10 seconds.
        - Prevents program from freezing due to any errors encountered during launch process.

    - Steam must be running to properly initialize launch process.

    ---

    :return: Start game client.
    :rtype: int | None
    """
    try:
        logger.info('Starting Valheim...\n\n')
        load("\nStarting Game", "Opening Valheim...")
        return call(r"C:\Program Files (x86)\Steam\Steam.exe -applaunch 892970", timeout=10)
    except TimeoutExpired as exp:
        logger.error(f'Something went wrong... Having trouble starting game...\n>> {exp}\n')
        print(f'Something went wrong... Having trouble starting game...\n>> {exp}\n')
        return _exitPatcher()


def _patch(patchDir: PathLike | str, targetDir: PathLike | str, patch_version: int | str) -> None:
    """Apply patch files (`patchDir`) to target directory (`targetDir`).

    - WILL overwrite existing files.

    ---

    :param patchDir: directory containing patch files.
    :type patchDir: Any
    :param targetDir: location of BepInEx install directory to install files.
    :type targetDir: Any
    :param patch_version: title of patch to be installed.
    :type patch_version: Any
    :return: patch BepInEx with files from desired version build.
    :rtype: None
    """
    try:
        logger.info(f'Patching BepInEx build {patch_version} to location: {targetDir}...\n')
        copytree(patchDir, targetDir, dirs_exist_ok=True)
        unlink(f'{globals.p_targetDir}/.gitkeep')
        load(
            f'\nPatching BepInEx build {patch_version} to location: {targetDir}',
            f'Patch build {patch_version} successfully installed!')
        logger.info(f'Patch build {patch_version} successfully installed!\n')
    except Exception as exc:
        logger.error(f'Something went wrong...\n>> {exc}\n>> Failed to successfully copy BepInEx build {patch_version} to location: {targetDir}...\n')
        print(f'Something went wrong...\n>> {exc}\n>> Failed to successfully copy BepInEx build {patch_version} to location: {targetDir}...')


def _UpdatePatcher():
    """Process to retrieve latest available patch files.

    ---

    :return: most recent release/build patch files.
    :rtype: None
    """
    DL.dl_stable(globals.url_stable)
    DL._unzip_patch(f'./patch-files/stable/BepInEx_stable_{globals.b_stable}.zip', True)
    DL.dl_dev(globals.url_dev)
    DL._unzip_patch(f'./patch-files/development/BepInEx_dev_{globals.b_dev}.zip', False)

    logger.info('Completed Patcher Update!\n>> Patches ready for deployment!\n')
    print('\nCompleted Patcher Update!\n>> Patches ready for deployment!\n')
    print('Press anything to continue...')
    m.getch()




def _exitPatcher() -> None | NoReturn:
    """Exit the application and finalize log.

    ---

    :return: Exits application.
    :rtype: None | NoReturn
    """
    logger.info(f'Exiting patcher...\n\n>> End of log...\n\n{globals._textborder}\n')
    return ex()


if __name__ == '__main__':
    VBPatcher()

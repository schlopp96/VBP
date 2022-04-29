#!/usr/bin/env python3

import logging
import os
import sys
from datetime import datetime
from os import chdir
from os.path import dirname
from shutil import copytree
from subprocess import TimeoutExpired, call
from sys import exit as ex
from time import sleep
from typing import Any, NoReturn
from zipfile import ZipFile

import requests
import tqdm
from PyLoadBar import load

#@ Declare global variables containing file locations and patch-install destinations:
chdir(dirname(__file__))

p_stable: str = './patch-files/stable'
p_dev: str = './patch-files/development'
b_stable: str = 'v5.19.00'
b_dev: str = 'da48b77'
p_targetDir: str = 'C:\Program Files (x86)\Steam\steamapps\common\Valheim'
_logFile: str = './logs/patchLog.log'
_datefmt: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
_textborder: str = "=".ljust((61),"=")
__version__: str = '0.6.0'

#* Establish Logger:
class LogGenerator():
    """Generates application loggers.

    - Uses built-in Python `logging` module.
    """
    def __init__(self, log_file: str, log_format: str = '[%(asctime)s - %(levelname)s] : %(message)s'):
        """Initialize logger instance

        :param log_file: file to write logs to.
        :type log_file: str
        :param log_format: formatting of log messages, defaults to '[%(asctime)s - %(levelname)s] : %(message)s'
        :type log_format: str, optional
        """
        self.logger = logging.getLogger(__name__)
        self.log_format = log_format
        self.formatter = logging.Formatter(log_format, datefmt="%Y-%m-%d %H:%M:%S")
        self.log_file = log_file
        self.fhandler = logging.FileHandler(log_file)
        self.logger.addHandler(self.fhandler)
        self.fhandler.setFormatter(self.formatter)
        self.logger.setLevel(logging.DEBUG)

    def debug(self, msg):
        return self.logger.debug(msg)
    def info(self, msg):
        return self.logger.info(msg)
    def warning(self, msg):
        return self.logger.warning(msg)
    def error(self, msg):
        return self.logger.error(msg)

logger = LogGenerator(_logFile)

#$ ====================================================================================================== $#


def VBPatcher() -> None | NoReturn:
    """Program entry point.

    ---

    :return: start VBPatcher.
    :rtype: None | NoReturn
    """
    logger.info(f'Welcome to the Valheim Bepinex Patcher v{__version__}!\n>> Session Start: {_datefmt}\n\n')
    while True:
        logger.info('Display user menu...')
        choosePatch: str = input(
            f"Welcome to the Valheim Bepinex Patcher!\n\nPlease Choose an Option by Entering its Corresponding Number:\n\n{_textborder}\n>> [1] Patch BepInEx to latest stable release: {b_stable} (2/3/22)\n>> [2] Patch BepInEx to latest development/expiremental build: {b_dev} (4/21/22)\n>> [3] Apply both patches to BepInEx in chronological order of release ({b_stable} then {b_dev})\n>> [4] Check for/update to newest patch versions\n>> [5] Open Valheim\n>> [6] Exit Program\n\n> "
        )
        match choosePatch:
            case '1': _patch_stable()
            case '2': _patch_dev()
            case '3': _patch_full()
            case '4': _UpdatePatcher()
            case '5': _openValheim()
            case '6':
                logger.info('BepInEx patching process cancelled...\n>> Preparing to exit...\n')
                load('\nBepInEx patching process cancelled', 'Preparing to exit...', enable_display=False)
                return _exitPatcher()
            case _:
                logger.warning(f'Invalid Input:\n>> "{choosePatch}"\n\n>> Must ONLY enter:\n>> [1] for stable release {b_stable}\n>> [2] for development build {b_dev}\n>> [3] for FULL upgrade (apply both patches in order of release)\n>> [4] to update available patch versions/builds\n>> [5] to open Valheim\n>> [6] to exit program\n')
                print(f'\n>> ERROR: Invalid Input -\n\n>> Your Entry:  "{choosePatch}".\n\n>> Must ONLY enter:\n>> [1] for stable release {b_stable}\n>> [2] for development build {b_dev}\n>> [3] for FULL upgrade (apply both patches in order of release)\n>> [4] to update available patch versions/builds\n>> [5] to open Valheim\n>> [6] to exit program\n\n')
                sleep(1.5)
                continue

        return _exitPatcher()

class _UpdateWrapper:
    """Wrapper containing patch-file update functionality.

    - Class Methods:
        - `dl_stable(self) -> BufferedWriter`
            - Download latest BepInEx stable release.
        - `dl_dev(self) -> BufferedWriter`
            - Download latest BepInEx development build.
    """
    def __init__(self) -> None:
        pass

    def dl_stable(self):
        """Download zip containing latest BepInEx stable release.

        :return: zip archive containing patch files.
        :rtype: BufferedWriter
        """
        url = 'https://github.com/BepInEx/BepInEx/releases/download/v5.4.19/BepInEx_x64_5.4.19.0.zip'

        while True:
            try:
                logger.info('Downloading latest BepInEx stable release...')
                rq = requests.get(url, allow_redirects=True, stream=True)
                file_size = int(rq.headers.get('Content-Length'))
                chunk_size = 1024  # 1 MB
                num_bars = file_size // chunk_size
                with open(f'./patch-files/stable/BepInEx_stable_{b_stable}.zip', 'wb') as patch_stable:
                    for chunk in tqdm.tqdm(rq.iter_content(chunk_size=chunk_size), total=num_bars, unit='KB', desc='Downloading Stable Release', file=sys.stdout):
                        patch_stable.write(chunk)
                    logger.info(f'Completed BepInEx latest stable-release download!\n>> Downloaded from url:\n>> {url}\n')
                    print(f'\nCompleted BepInEx latest stable-release download!\n>> Downloaded from url:\n>> {url}\n')
                return patch_stable

            except [requests.exceptions.RequestException, requests.exceptions.ConnectionError, requests.exceptions.Timeout, requests.exceptions.HTTPError, requests.exceptions.InvalidURL] as err:
                logger.error(f'Encountered error while downloading latest stable release zip archive...\n>> Exception: {err}\n')
                print(f'Encountered error while downloading latest stable release zip archive...\n>> Exception: {err}\n')

                while True:
                    logger.info('Displaying retry update-check prompt...')
                    again = input('\nTry again? [y/n]:\n>> ')
                    match again.lower():
                        case 'y':
                            continue
                        case _:
                            print('\n>> Cancelled update-check.\n')
                            break

    def dl_dev(self):
        """Download zip archive containing latest BepInEx development build.

        :return: zip archive containing patch files.
        :rtype: BufferedWriter
        """
        url = 'https://builds.bepinex.dev/projects/bepinex_be/557/BepInEx_UnityMono_x64_da48b77_6.0.0-be.557.zip'
        while True:
            try:
                logger.info('Downloading latest BepInEx development-build...')
                rq = requests.get(url, allow_redirects=True, stream=True)
                file_size = int(rq.headers.get('Content-Length'))
                chunk_size = 1024  # 1 MB
                num_bars = file_size // chunk_size
                with open(f'./patch-files/development/BepInEx_dev_{b_dev}.zip', 'wb') as patch_stable:
                    for chunk in tqdm.tqdm(rq.iter_content(chunk_size=chunk_size), total=num_bars, unit='KB', desc='Downloading Dev-Build', file=sys.stdout):
                        patch_stable.write(chunk)
                    logger.info(f'Completed BepInEx latest development-build download!\n>> Downloaded from url:\n>> {url}\n')
                    print(f'\nCompleted BepInEx latest development-build download!\n>> Downloaded from url:\n>> {url}\n')
                return patch_stable

            except [requests.exceptions.RequestException, requests.exceptions.ConnectionError, requests.exceptions.Timeout, requests.exceptions.HTTPError, requests.exceptions.InvalidURL] as err:
                logger.error(f'Encountered error while downloading latest development-build zip archive...\n>> Exception: {err}\n')
                print(f'Encountered error while downloading latest development-build zip archive...\n>> Exception: {err}')

                while True:
                    logger.info('Displaying retry update-check prompt...')
                    again = input('\nTry again? [y/n]:\n>> ')
                    match again.lower():
                        case 'y':
                            continue
                        case _:
                            print('\n>> Cancelled update-check.\n')
                            break

    def _unzip_patch(self, filename, stable: bool) -> None:
        """Unzip downloaded patch files before deleting patch `.zip` archive.

        ---

        :param filename: filename of zip archive.
        :type filename: str | PathLike
        :param stable: determines whether or not zip archive contains files for BepInEx STABLE release patch. False if contains DEVELOPMENT build patch files.
        :type stable: bool
        :return: downloaded/extracted patch files.
        :rtype: None
        """
        logger.info('Unzipping patch files...')
        print('Unzipping patch files...')
        try:
            if stable:
                with ZipFile(filename) as archive:
                        archive.extractall(path='./patch-files/stable')
                os.unlink('./patch-files/stable/doorstop_config.ini')
                os.unlink(f'./patch-files/stable/BepInEx_stable_{b_stable}.zip')
            else:
                with ZipFile(filename) as archive:
                    archive.extractall(path='./patch-files/development')
                os.unlink('./patch-files/development/doorstop_config.ini')
                os.unlink(f'./patch-files/development/BepInEx_dev_{b_dev}.zip')

            logger.info('Successfully unzipped archive!\n>> Deleted extra files...\n>> Patch ready for deployment!\n')
            print('\n>> Successfully unzipped archive!\n>> Deleted extra files...\n>> Patch ready for deployment!\n')

        except Exception as err:
            logger.error(f'Encountered error while attempting to unzip archive...\n>> Exception: {err}\n')
            print(f'Encountered error while attempting to unzip archive...\n>> Exception: {err}\n')


UpdateDL = _UpdateWrapper()


def _patch_stable() -> None | NoReturn:
    """Install latest BepInEx stable-build release version to local directory.

    ---

    :return: patched BepInEx installation.
    :rtype: None
    """
    while True:
        logger.info(f'Displaying confirmation prompt to install BepInEx {b_stable} release...')
        confirmStable: str = input(
            f'\nReally patch BepInEx to latest stable-release {b_stable} in location:\n\n>> "{p_targetDir}"?\n\n> Enter [y] or [n]:\n{_textborder}\n> '
        )
        match confirmStable.lower():
            case 'yes'|'y':
                _patch(p_stable, p_targetDir, b_stable)
                _startPrompt()
            case 'n'|'no':
                logger.info('BepInEx patching process cancelled...\n>> Preparing to exit...\n')
                load('\nBepInEx patching process cancelled', 'Preparing to exit...', enable_display=False)
                return _exitPatcher()
            case _:
                logger.warning(f'Invalid Input: "{confirmStable}"\n>> Must ONLY enter either [y] for "YES" or [n] for "NO".\n')
                print(f'\n>> ERROR: Invalid Input\n\n>> Your Entry: "{confirmStable}".\n\n>> Must ONLY enter either [y] for "YES" or [n] for "NO".\n\n')
                sleep(1.250)
                continue


def _patch_dev() -> None | NoReturn:
    """Install latest BepInEx development patch version to local directory.

    ---

    :return: patched BepInEx installation.
    :rtype: None
    """
    while True:
        logger.info(f'Displaying confirmation prompt to install BepInEx development build {b_dev} patch...')
        confirmLatest: str = input(
            f'\nReally patch BepInEx to latest development build {b_dev} in location:\n\n>> "{p_targetDir}"?\n\n> Enter [y] or [n]:\n{_textborder}\n> '
        )
        match confirmLatest.lower():
            case 'yes'|'y':
                _patch(p_stable, p_targetDir, b_dev)
                _startPrompt()
            case 'n'|'no':
                logger.info('BepInEx patching process cancelled...\n>> Preparing to exit...\n')
                load('\nBepInEx patching process cancelled', 'Preparing to exit...', enable_display=False)
                return _exitPatcher()
            case _:
                logger.warning(f'Invalid Input: "{confirmLatest}"\n>> Must ONLY enter either [y] for "YES" or [n] for "NO".\n')
                print(f'\n>> ERROR: Invalid Input\n\n>> Your Entry: "{confirmLatest}".\n\n>> Must ONLY enter either [y] for "YES" or [n] for "NO".\n\n')
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
            f'\nReally apply both latest stable release {b_stable}, and latest development build {b_dev} patches?\n> Enter [y] or [n]:\n{_textborder}\n> '
        )
        match confirmFull.lower():
            case 'yes'|'y':
                _patch(p_stable, p_targetDir, b_stable)
                _patch(p_dev, p_targetDir, b_dev)
                return _startPrompt()
            case 'n'|'no':
                logger.info('BepInEx patching process cancelled...\n>> Preparing to exit...\n')
                load('\n>> BepInEx patching process cancelled', '>> Preparing to exit...', enable_display=False)
                return _exitPatcher()
            case _:
                logger.warning(f'Invalid Input: "{confirmFull}"\n>> Must ONLY enter either [y] for "YES" or [n] for "NO".\n')
                print(f'\n>> ERROR: Invalid Input\n\n>> Your Entry: "{confirmFull}".\n\n>> Must ONLY enter either [y] for "YES" or [n] for "NO".\n\n')
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
            f'\nStart Game?\n\n> Enter [y] or [n]:\n{_textborder}\n> ')
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
                print(f'\n>> ERROR: Invalid Input\n\n>> Your Entry: "{startPrompt}".\n\n>> Must ONLY enter either [y] for "YES" or [n] for "NO".\n\n')
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


def _patch(patchDir: Any, targetDir: Any, ver: Any) -> None:
    """Apply patch files (`patchDir`) to target directory (`targetDir`).

    - WILL overwrite existing files.

    ---

    :param patchDir: directory containing patch files.
    :type patchDir: Any
    :param targetDir: location of BepInEx install directory to install files.
    :type targetDir: Any
    :param ver: title of patch to be installed.
    :type ver: Any
    :return: patch BepInEx with files from desired version build.
    :rtype: None
    """
    try:
        logger.info(f'Patching BepInEx build {ver} to location: {targetDir}...\n')
        load(
            f'\nPatching BepInEx build {ver} to location: {targetDir}',
            f'\nPatch build {ver} successfully installed!')
        copytree(patchDir, targetDir, dirs_exist_ok=True)
        logger.info(f'Patch build {ver} successfully installed!\n')
    except Exception as exc:
        logger.error(f'Something went wrong...\n>> {exc}\n>> Failed to successfully copy BepInEx build {ver} to location: {targetDir}...\n')
        print(f'Something went wrong...\n>> {exc}\n>> Failed to successfully copy BepInEx build {ver} to location: {targetDir}...')


def _UpdatePatcher() -> None:
    """Process to retrieve latest available patch files.

    ---

    :return: most recent release/build patch files.
    :rtype: None
    """
    UpdateDL.dl_stable()
    UpdateDL._unzip_patch(f'./patch-files/stable/BepInEx_stable_{b_stable}.zip', True)
    UpdateDL.dl_dev()
    UpdateDL._unzip_patch(f'./patch-files/development/BepInEx_dev_{b_dev}.zip', False)

    logger.info('Completed Patcher Update!\n>> Restart program to use updated patch files.\n')
    print('\n>> Completed Patcher Update!\n>> Restart program to use updated patch files..\n')
    input('Press [ENTER] to exit application.\n')



def _exitPatcher() -> None | NoReturn:
    """Exit the application and finalize log.

    ---

    :return: Exits application.
    :rtype: None | NoReturn
    """
    logger.info(f'Exiting patcher...\n\n>> End of log...\n\n\n{_textborder}\n\n')
    return ex()


if __name__ == '__main__':
    VBPatcher()

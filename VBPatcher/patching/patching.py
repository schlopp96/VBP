from os import PathLike, unlink
from shutil import copytree
from time import sleep
from typing import NoReturn

import applogger.applogger
import globalvars.globalvars
from PyLoadBar import load
from subprocessing.subprocessing import _exitPatcher, _startPrompt

logger = applogger.applogger._LogGenerator(globalvars.globalvars._logFile)


class _Patcher:
    """Wrapper to handle patch functionality.

    - Contains the following patching methods:
        - `_patch_stable(self) -> None | NoReturn`
            - Install latest BepInEx stable-build release version to local directory.
        - `_patch_dev(self) -> None | NoReturn`
            - Install latest BepInEx development build version to local directory.
        - `_patch_full() -> None | NoReturn`
            - Apply both available BepInEx patches in order of release (Stable -> Development).
        - `_patch(self, patchDir: PathLike | str, targetDir: PathLike | str, patch_version: int | str) -> None`
            - Apply patch files (`patchDir`) to target directory (`targetDir`).
    """

    def __init__(self):
        pass

    def _patch(self, patchDir: PathLike | str, targetDir: PathLike | str, patch_version: int | str) -> None:
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
            unlink(f'{globalvars.globalvars.p_targetDir}/.gitkeep')
            load(
                f'\nPatching BepInEx build {patch_version} to location: {targetDir}',
                f'Patch build {patch_version} successfully installed!')
            logger.info(f'Patch build {patch_version} successfully installed!\n')
        except Exception as exc:
            logger.error(f'Something went wrong...\n>> {exc}\n>> Failed to successfully copy BepInEx build {patch_version} to location: {targetDir}...\n')
            print(f'Something went wrong...\n>> {exc}\n>> Failed to successfully copy BepInEx build {patch_version} to location: {targetDir}...')

    def _patch_stable(self) -> None | NoReturn:
        """Install latest BepInEx stable-build release version to local directory.

        ---

        :return: patched BepInEx installation.
        :rtype: None
        """
        while True:
            logger.info(f'Prompting user for installation of BepInEx stable release {globalvars.globalvars.b_dev} patch...')
            confirmStable: str = input(
                f'\nReally patch BepInEx to latest stable-release {globalvars.globalvars.b_stable} in location:\n\n>> "{globalvars.globalvars.p_targetDir}"?\n\n> Enter [y] or [n]:\n{globalvars.globalvars._textborder}\n> '
            )
            match confirmStable.lower():
                case 'yes'|'y':
                    self._patch(globalvars.globalvars.p_stable, globalvars.globalvars.p_targetDir, globalvars.globalvars.b_stable)
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


    def _patch_dev(self) -> None | NoReturn:
        """Install latest BepInEx development patch version to local directory.

        ---

        :return: patched BepInEx installation.
        :rtype: None
        """
        while True:
            logger.info(f'Prompting user for installation of BepInEx development build {globalvars.globalvars.b_dev} patch...')
            confirmLatest: str = input(
                f'\nReally patch BepInEx to latest development build {globalvars.globalvars.b_dev} in location:\n\n>> "{globalvars.globalvars.p_targetDir}"?\n\n> Enter [y] or [n]:\n{globalvars.globalvars._textborder}\n> '
            )
            match confirmLatest.lower():
                case 'yes'|'y':
                    self._patch(globalvars.globalvars.p_dev, globalvars.globalvars.p_targetDir, globalvars.globalvars.b_dev)
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


    def _patch_full(self) -> None | bool:
        """Apply both available BepInEx patches in order of release (Stable -> Development).

        ---

        :return: patched BepInEx installation.
        :rtype: None
        """
        while True:
            logger.info('Displaying confirmation prompt to install full-upgrade patch (install both stable and development builds in order of release)...')
            confirmFull: str = input(
                f'\nReally apply both latest stable release {globalvars.globalvars.b_stable}, and latest development build {globalvars.globalvars.b_dev}?\n> Enter [y] or [n]:\n{globalvars.globalvars._textborder}\n> '
            )
            match confirmFull.lower():
                case 'yes'|'y':
                    self._patch(globalvars.globalvars.p_stable, globalvars.globalvars.p_targetDir, globalvars.globalvars.b_stable)
                    self._patch(globalvars.globalvars.p_dev, globalvars.globalvars.p_targetDir, globalvars.globalvars.b_dev)
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

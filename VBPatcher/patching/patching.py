from os import PathLike, unlink
from shutil import copytree
from time import sleep
from typing import NoReturn

import PyLoadBar
import VBPatcher.globalvars.globalvars
from VBPatcher.applogger.applogger import logger
from VBPatcher.subprocessing.subprocessing import _exitPatcher, _startPrompt

bar = PyLoadBar.PyLoadBar()

class _Patcher:
    """Wrapper to handle patch functionality.

    - Contains the following patching methods:
        - `_patch(self, patch_src: PathLike | str, patch_dst: PathLike | str, patch_ver: int | str) -> None`
            - Install patch files (`patch_src`) to target directory (`patch_dst`).

        - `_patch_stable(self) -> None | NoReturn`
            - Install latest BepInEx stable release version to target directory.

        - `_patch_dev(self) -> None | NoReturn`
            - Install latest BepInEx development build version to target directory.

        - `_patch_full() -> None | NoReturn`
            - Apply both available BepInEx patches in order of release (Stable -> Development).
    """

    def __init__(self):
        pass

    def _patch(self, patch_src: PathLike | str, patch_dst: PathLike | str, patch_ver: int | str) -> None:
        """Apply patch files (`patch_src`) to target directory (`patch_dst`).

        - Overwrites any existing patch files.

        ---

        :param patch_src: source directory containing patch files.
        :type patch_src: Any
        :param patch_dst: destination of patch files.
        :type patch_dst: Any
        :param patch_ver: version/title/build of patch.
        :type patch_ver: Any
        :return: transfer patch files from `patch_src` to `patch_dst`.
        :rtype: None
        """
        try:
            logger.info(f'Patching BepInEx build {patch_ver} to location: {patch_dst}...\n')
            copytree(patch_src, patch_dst, dirs_exist_ok=True)
            unlink(f'{VBPatcher.globalvars.globalvars.p_targetDir}/.gitkeep')
            bar.load(
                f'\nPatching BepInEx build {patch_ver} to location: {patch_dst}',
                f'Patch build {patch_ver} successfully installed!', label='Patching')
            logger.info(f'Patch build {patch_ver} successfully installed!\n')
        except Exception as exc:
            logger.error(f'Something went wrong...\n>> {exc}\n>> Failed to successfully copy BepInEx build {patch_ver} to location: {patch_dst}...\n')
            print(f'Something went wrong...\n>> {exc}\n>> Failed to successfully copy BepInEx build {patch_ver} to location: {patch_dst}...')

    def _patch_stable(self) -> None | NoReturn:
        """Install latest BepInEx stable-build release version to local directory.

        ---

        :return: patched BepInEx installation.
        :rtype: None
        """
        while True:
            logger.info(f'Prompting user for installation of BepInEx stable release {VBPatcher.globalvars.globalvars.b_dev} patch...')
            confirmStable: str = input(
                f'\nReally patch BepInEx to latest stable-release {VBPatcher.globalvars.globalvars.b_stable} in location:\n\n>> "{VBPatcher.globalvars.globalvars.p_targetDir}"?\n\n> Enter [y] or [n]:\n{VBPatcher.globalvars.globalvars._textborder}\n> '
            )
            match confirmStable.lower():
                case 'yes'|'y':
                    self._patch(VBPatcher.globalvars.globalvars.p_stable, VBPatcher.globalvars.globalvars.p_targetDir, VBPatcher.globalvars.globalvars.b_stable)
                    _startPrompt()
                case 'n'|'no':
                    logger.info('BepInEx patching process cancelled...\n>> Preparing to exit...\n')
                    bar.load('\nBepInEx patching process cancelled', 'Preparing to exit...', enable_display=False)
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
            logger.info(f'Prompting user for installation of BepInEx development build {VBPatcher.globalvars.globalvars.b_dev} patch...')
            confirmLatest: str = input(
                f'\nReally patch BepInEx to latest development build {VBPatcher.globalvars.globalvars.b_dev} in location:\n\n>> "{VBPatcher.globalvars.globalvars.p_targetDir}"?\n\n> Enter [y] or [n]:\n{VBPatcher.globalvars.globalvars._textborder}\n> '
            )
            match confirmLatest.lower():
                case 'yes'|'y':
                    self._patch(VBPatcher.globalvars.globalvars.p_dev, VBPatcher.globalvars.globalvars.p_targetDir, VBPatcher.globalvars.globalvars.b_dev)
                    _startPrompt()
                case 'n'|'no':
                    logger.info('BepInEx patching process cancelled...\n>> Preparing to exit...\n')
                    bar.load('\nBepInEx patching process cancelled', 'Preparing to exit...', enable_display=False)
                    return _exitPatcher()
                case _:
                    logger.warning(f'Invalid Input: "{confirmLatest}"\n>> Must ONLY enter either [y] for "YES" or [n] for "NO".\n')
                    print(f'\nERROR: Invalid Input\n\n>> Your Entry: "{confirmLatest}".\n\n>> Must ONLY enter either [y] for "YES" or [n] for "NO".\n\n')
                    sleep(1.250)
                    continue


    def _patch_full(self) -> None | bool:
        """Apply both stable and dev BepInEx patches in order of release (Stable -> Development).

        ---

        :return: patched BepInEx installation.
        :rtype: None
        """
        while True:
            logger.info('Displaying confirmation prompt to install full-upgrade patch (install both stable and development builds in order of release)...')
            confirmFull: str = input(
                f'\nReally apply both latest stable release {VBPatcher.globalvars.globalvars.b_stable}, and latest development build {VBPatcher.globalvars.globalvars.b_dev}?\n> Enter [y] or [n]:\n{VBPatcher.globalvars.globalvars._textborder}\n> '
            )
            match confirmFull.lower():
                case 'yes'|'y':
                    self._patch(VBPatcher.globalvars.globalvars.p_stable, VBPatcher.globalvars.globalvars.p_targetDir, VBPatcher.globalvars.globalvars.b_stable)
                    self._patch(VBPatcher.globalvars.globalvars.p_dev, VBPatcher.globalvars.globalvars.p_targetDir, VBPatcher.globalvars.globalvars.b_dev)
                    return _startPrompt()
                case 'n'|'no':
                    logger.info('BepInEx patching process cancelled...\n>> Preparing to exit...\n')
                    bar.load('\n>> BepInEx patching process cancelled', '>> Preparing to exit...', enable_display=False)
                    return _exitPatcher()
                case _:
                    logger.warning(f'Invalid Input: "{confirmFull}"\n>> Must ONLY enter either [y] for "YES" or [n] for "NO".\n')
                    print(f'\nERROR: Invalid Input\n\n>> Your Entry: "{confirmFull}".\n\n>> Must ONLY enter either [y] for "YES" or [n] for "NO".\n\n')
                    sleep(1.250)
                    continue

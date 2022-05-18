import os

import VBPatcher.applogger.applogger
import VBPatcher.downloader.downloader
import VBPatcher.globalvars.globalvars
from PyLoadBar import load
from VBPatcher.subprocessing.subprocessing import _exitPatcher

logger = VBPatcher.applogger.applogger._LogGenerator(VBPatcher.globalvars.globalvars._logFile)
DL = VBPatcher.downloader.downloader._Downloader()


class _Validate:
    """Wrapper for validation of required BepInEx patch files.

    Contains the following methods:
        - `_verify_dev`: verifies presence of BepInEx dev release patch files.
        - `_verify_stable`: verifies presence of BepInEx stable release patch files.
        - `_start_checks`: verifies presence of all BepInEx patch-files upon start.
    """

    def __init__(self):
        pass

    def _verify_stable(self, url) -> bool:
        """Validate presence of BepInEx stable release patch files.

        :param url: url to download BepInEx stable release from if not found.
        :type url: Any
        :return: validation of patch files.
        :rtype: bool
        """
        logger.info(
            f'Validating stable-build {VBPatcher.globalvars.globalvars.b_stable} patch files...\n'
        )

        stable_files: list = [
            ['.gitkeep', 'changelog.txt', 'winhttp.dll'], [],
            [
                '0Harmony.dll', '0Harmony.xml', '0Harmony20.dll',
                'BepInEx.dll', 'BepInEx.Harmony.dll', 'BepInEx.Harmony.xml',
                'BepInEx.Preloader.dll', 'BepInEx.Preloader.xml',
                'BepInEx.xml', 'HarmonyXInterop.dll', 'Mono.Cecil.dll',
                'Mono.Cecil.Mdb.dll', 'Mono.Cecil.Pdb.dll',
                'Mono.Cecil.Rocks.dll', 'MonoMod.RuntimeDetour.dll',
                'MonoMod.RuntimeDetour.xml', 'MonoMod.Utils.dll',
                'MonoMod.Utils.xml'
            ]
        ]

        stable_match: bool = False

        found: list = []

        try:
            found.extend(
                file
                for (root, dirs,
                     file) in os.walk('./patch-files/stable', topdown=True))
            if found == stable_files:
                stable_match = True
                logger.info(
                    f'Stable-build {VBPatcher.globalvars.globalvars.b_stable} patch files verified successfully!\n'
                )

            else:
                logger.info(
                    f'Unable to verify stable patch {VBPatcher.globalvars.globalvars.b_stable} files...\n>> Attempting to download...\n'
                )
                DL.dl_stable(url)
                DL._unzip_patch(
                    f'./patch-files/stable/BepInEx_stable_{VBPatcher.globalvars.globalvars.b_stable}.zip',
                    True)
                stable_match = True
                logger.info(
                    f'Successfully downloaded stable-build {VBPatcher.globalvars.globalvars.b_stable} patch files!\n'
                )
            return stable_match

        except Exception as err:
            stable_match = False
            logger.error(
                f'Encountered error during application start checks...\n>> Exception: {err}\n'
            )

        finally:
            return stable_match

    def _verify_dev(self, url) -> bool:
        """Validate presence of BepInEx development build patch files.

        :param url: url to download BepInEx development build from if not found.
        :type url: PathLike | str
        :return: validation of patch files.
        :rtype: bool
        """
        logger.info(
            f'Validating development patch {VBPatcher.globalvars.globalvars.b_dev} files...\n'
        )

        dev_files: list = [
            ['.gitkeep', 'changelog.txt', 'winhttp.dll'], [],
            [
                '0Harmony.dll', 'BepInEx.Core.dll', 'BepInEx.Core.xml',
                'BepInEx.Preloader.Core.dll', 'BepInEx.Preloader.Core.xml',
                'BepInEx.Preloader.Unity.dll', 'BepInEx.Preloader.Unity.xml',
                'BepInEx.Unity.dll', 'BepInEx.Unity.xml', 'Mono.Cecil.dll',
                'Mono.Cecil.Mdb.dll', 'Mono.Cecil.Pdb.dll',
                'Mono.Cecil.Rocks.dll', 'MonoMod.RuntimeDetour.dll',
                'MonoMod.Utils.dll', 'SemanticVersioning.dll'
            ]
        ]

        dev_match: bool = False

        found: list = []

        try:
            found.extend(file for (
                root, dirs,
                file) in os.walk('./patch-files/development/', topdown=True))
            if found == dev_files:
                dev_match = True
                logger.info(
                    f'Development patch {VBPatcher.globalvars.globalvars.b_dev} files verified successfully!\n'
                )

            else:
                logger.info(
                    f'Unable to verify development patch {VBPatcher.globalvars.globalvars.b_dev} files...\n>> Attempting to download...\n'
                )
                DL.dl_dev(url)
                DL._unzip_patch(
                    f'./patch-files/development/BepInEx_dev_{VBPatcher.globalvars.globalvars.b_dev}.zip',
                    False)
                dev_match = True
                logger.info(
                    f'Successfully downloaded development patch {VBPatcher.globalvars.globalvars.b_dev} files!\n'
                )
            return dev_match

        except Exception as err:
            dev_match = False
            logger.error(
                f'Encountered error during application start checks...\n>> Exception: {err}\n'
            )

        finally:
            return dev_match

    def _start_checks(self) -> None:
        """Verify application has latest BepInEx patches upon start.

        :return: continue to application if verification is successful, otherwise exits program.
        :rtype: None
        """
        logger.info('Checking for application BepInEx patch files...\n')

        if self._verify_stable(
                VBPatcher.globalvars.globalvars.url_stable) and self._verify_dev(
                    VBPatcher.globalvars.globalvars.url_dev):
            logger.info('Successfully verified BepInEx patch files!\n')
        else:
            logger.info(
                'One or more patch files were not able to be verified...')
            load('ERROR: One or more patch files were not able to be verified',
                 'Exiting Patcher',
                 enable_display=False)
            return _exitPatcher()

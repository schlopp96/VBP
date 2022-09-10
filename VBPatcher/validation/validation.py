import os
from zipfile import is_zipfile

import VBPatcher.appglobals.globals
import VBPatcher.downloader.downloader
from PyLoadBar import PyLoadBar
from VBPatcher.apploggers.loggers import logger, logger_stream
from VBPatcher.subprocessing.subprocessing import _exitPatcher

DL = VBPatcher.downloader.downloader._Downloader()
bar = PyLoadBar(False)


class _Validate:
    """Validate location and deployability of necessary patch files.

    ---

    - Contains the following validation methods:

        - :func:`_validate_stable(url) -> bool`
            - Validate presence of BepInEx stable build patch files.
            - Static method.

        - :func:`_validate_dev(url) -> bool:`
            - Validate presence of BepInEx dev build patch files.
            - Static method.

        - :func:`_start_checks(self) -> None`
            - Start patch file validation checks.
    """

    @staticmethod
    def _validate_stable(url) -> bool:
        """Validate presence of BepInEx stable build patch files.

        ---

        :param url: url to download BepInEx stable build from if not found.
        :type url: :class:`Any`
        :return: validation of patch files.
        :rtype: :class:`bool`
        """

        logger.info(
            f'Validating BepInEx stable-build {VBPatcher.appglobals.globals.ver_stable} patch...'
        )

        patch_contents: list = [
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
        ]  # List of files to verify

        stable_match: bool = False  # Initialize match flag

        verified: list = []  # Initialize verified file list

        try:
            verified.extend(
                file
                for (root, dirs,
                     file) in os.walk('./patch-files/stable', topdown=True
                                      ))  # Get list of files in patch folder

            if verified == patch_contents:
                stable_match = True
                logger.info(
                    f'BepInEx stable-build {VBPatcher.appglobals.globals.ver_stable} patch ready for deployment!\n'
                )

            else:
                logger.info(
                    f'Unable to locate BepInEx stable-build {VBPatcher.appglobals.globals.ver_stable} patch...\n>> Attempting to download...'
                )
                DL._dl_stable(url)  # Download *.zip archive from url

                if is_zipfile(
                        f'./patch-files/stable/BepInEx_stable_{VBPatcher.appglobals.globals.ver_stable}.zip'
                ):  # Check if downloaded archive is a zip file
                    DL._unzip_patch(  # Unzip archive
                        f'./patch-files/stable/BepInEx_stable_{VBPatcher.appglobals.globals.ver_stable}.zip',
                        1)
                    stable_match = True  # Update match flag
                    logger.info(
                        f'Download successful!\n>> BepInEx stable-build {VBPatcher.appglobals.globals.ver_stable} patch ready for deployment!\n'
                    )

                else:
                    stable_match = False  # Update match flag
                    logger.error(
                        'Download failed!\n>> BepInEx dev-build patch unable to be deployed!\n'
                    )

        except Exception:
            stable_match = False
            logger.error(
                f'Encountered error during BepInEx stable-build {VBPatcher.appglobals.globals.ver_stable} patch validation...\n'
            )

        finally:
            return stable_match  # Return result of validation

    @staticmethod
    def _validate_dev(url) -> bool:
        """Validate presence of BepInEx development build patch files.

        ---

        :param url: url to download BepInEx development build from if not found.
        :type url: :class:`PathLike` | :class:`str`
        :return: validation of patch files.
        :rtype: :class:`bool`
        """

        logger.info(
            f'Validating BepInEx dev-build {VBPatcher.appglobals.globals.ver_dev} patch...'
        )

        patch_contents: list = [
            ['.doorstop_version', '.gitkeep', 'changelog.txt', 'winhttp.dll'],
            [],
            [
                '0Harmony.dll', 'AssetRipper.VersionUtilities.dll',
                'BepInEx.Core.dll', 'BepInEx.Core.xml',
                'BepInEx.Preloader.Core.dll', 'BepInEx.Preloader.Core.xml',
                'BepInEx.Unity.Common.dll', 'BepInEx.Unity.Common.xml',
                'BepInEx.Unity.Mono.dll', 'BepInEx.Unity.Mono.Preloader.dll',
                'BepInEx.Unity.Mono.Preloader.xml', 'BepInEx.Unity.Mono.xml',
                'Mono.Cecil.dll', 'Mono.Cecil.Mdb.dll', 'Mono.Cecil.Pdb.dll',
                'Mono.Cecil.Rocks.dll', 'MonoMod.RuntimeDetour.dll',
                'MonoMod.Utils.dll', 'SemanticVersioning.dll'
            ], [], []
        ]  # List of files to verify

        dev_match: bool = False  # Initialize match flag

        verified: list = []  # Initialize verified file list

        try:
            verified.extend(file for (
                root, dirs,
                file) in os.walk('./patch-files/development/', topdown=True)
                            )  # Get list of files in patch folder

            if verified == patch_contents:
                dev_match = True  # Update match flag
                logger.info(
                    f'BepInEx dev-build {VBPatcher.appglobals.globals.ver_dev} patch ready for deployment!\n'
                )

            else:
                logger.info(
                    f'Unable to locate BepInEx dev-build {VBPatcher.appglobals.globals.ver_dev} patch...\n>> Attempting to download...'
                )
                DL._dl_dev(url)  # Download *.zip file from url

                if is_zipfile(  # Check if downloaded archive is a zip file
                        f'./patch-files/development/BepInEx_dev_{VBPatcher.appglobals.globals.ver_dev}.zip'
                ):
                    DL._unzip_patch(  # Unzip archive
                        f'./patch-files/development/BepInEx_dev_{VBPatcher.appglobals.globals.ver_dev}.zip',
                        2)

                    dev_match = True  # Update match flag
                    logger.info(
                        f'Download successful!\n>> BepInEx dev-build {VBPatcher.appglobals.globals.ver_dev} patch ready for deployment!\n'
                    )

                else:  # If download failed
                    dev_match = False  # Update match flag
                    logger.error(
                        'Download failed!\n>> BepInEx dev-build patch unable to be deployed!\n'
                    )

        except Exception:
            dev_match = False
            logger.error(
                f'Encountered error during BepInEx dev-build {VBPatcher.appglobals.globals.ver_dev} patch validation...\n'
            )

        finally:
            return dev_match  # Return result of validation

    def _start_checks(self) -> None:
        """Verify necessary patcher components upon start.

        - If any patch files are missing, attempt to download them.

        ---

        :return: continue to application if verification is successful, otherwise exits program.
        :rtype: None
        """

        logger_stream.info('Initializing VBPatcher start checks...\n')

        if self._validate_stable(VBPatcher.appglobals.globals.url_stable
                                 ) and self._validate_dev(
                                     VBPatcher.appglobals.globals.url_dev
                                 ):  # Validate presence of patch files
            logger_stream.info(
                'VBPatcher start checks completed successfully!\n')

        else:

            logger_stream.error(
                'VBPatcher start checks failed!\n>> One or more patch files were unable to be verified and are unable to be deployed...\n\n>> Press anything to continue...\n'
            )
            VBPatcher.appglobals.globals.getch(
            )  # Wait for user input to continue

            bar.start('>> Exiting VBPatcher',
                      '>> VBPatcher has exited successfully!',
                      iter_total=3,
                      txt_iter_speed=0.25)

            return _exitPatcher()  # Exit program

import msvcrt as m
import os
import sys
from os import PathLike
from urllib.error import HTTPError
from zipfile import ZipFile

import requests
import tqdm
import VBPatcher.appglobals.globals
from requests import Response
from VBPatcher.apploggers.loggers import logger, logger_stream


class _Downloader:
    """Wrapper containing patch-file update functionality.

    ---

	- Contains the following download methods:

		- :func:`_dl_stable(self, url) -> BufferedWriter`
			- Download latest BepInEx stable release.
            - Static method.

		- :func:`_dl_dev(self, url) -> BufferedWriter`
			- Download latest BepInEx development build.
            - Static method.

		- :func:`_unzip_patch(self, filename, stable) -> None`
			- Unzip downloaded patch files before deleting patch `.zip` archive.
            - Static method.

		- :func:`UpdatePatcher(self) -> None`
			- Process to retrieve latest available patch files using class methods.
	"""

    @staticmethod
    def _dl_stable(url):
        """Download zip containing latest BepInEx stable release.

		---

		:param url: URL from which to download zip archive.
		:type url: :class:`str`
		:return: zip archive containing patch files.
		:rtype: :class:`BufferedWriter`
		"""

        logger.info('Downloading latest BepInEx stable release...')

        try:
            rq: Response = requests.get(url, allow_redirects=True,
                                        stream=True)  # Download zip archive
            rq.raise_for_status()  # Check for HTTP errors

            file_size: int = int(rq.headers.get('Content-Length'))  # File size
            chunk_size: int = 1024  # 1 MB
            prog_max: int = file_size // chunk_size  # Calculate progress bar max

            with open(
                    f'./patch-files/stable/BepInEx_stable_{VBPatcher.appglobals.globals.b_stable}.zip',
                    'wb') as patch_stable:
                for chunk in tqdm.tqdm(rq.iter_content(chunk_size=chunk_size),
                                       total=prog_max,
                                       unit='KB',
                                       desc='Downloading Stable Release',
                                       file=sys.stdout):
                    patch_stable.write(chunk)

            logger_stream.info(
                f'>> Completed BepInEx latest stable-release download!\n\n>> Downloaded from url:\n>> {url}\n'
            )
            return patch_stable

        except [Exception, HTTPError] as err:
            logger_stream.error(
                f'Encountered error while downloading latest stable release zip archive...\n\n>> Exception:\n{err}\n'
            )

    @staticmethod
    def _dl_dev(url):
        """Download zip archive containing latest BepInEx development build.

		---

		:param url: URL from which to download zip archive.
		:type url: :class:`str`
		:return: zip archive containing patch files.
		:rtype: :class:`BufferedWriter`
		"""

        logger.info('Downloading latest BepInEx development-build...')

        try:
            rq: Response = requests.get(url, allow_redirects=True,
                                        stream=True)  # Download zip archive
            rq.raise_for_status()  # Check for HTTP errors

            file_size: int = int(rq.headers.get('Content-Length'))  # File size
            chunk_size: int = 1024  # 1 MB
            prog_max: int = file_size // chunk_size  # Calculate progress bar max

            with open(
                    f'./patch-files/development/BepInEx_dev_{VBPatcher.appglobals.globals.b_dev}.zip',
                    'wb') as patch_dev:
                for chunk in tqdm.tqdm(rq.iter_content(chunk_size=chunk_size),
                                       total=prog_max,
                                       unit='KB',
                                       desc='Downloading Dev-Build',
                                       file=sys.stdout):
                    patch_dev.write(chunk)

                logger_stream.info(
                    f'>> Completed BepInEx latest development-build download!\n\n>> Downloaded from url:\n>> {url}\n'
                )
            return patch_dev

        except [Exception, HTTPError] as err:
            logger_stream.error(
                f'Encountered error while downloading latest development-build zip archive...\n\n>> Exception:\n{err}\n'
            )

    @staticmethod
    def _unzip_patch(filename: PathLike | str, mode: int) -> None:
        """Unzip downloaded patch files and cleanup leftover files.

		---

		:param filename: filename of zip archive.
		:type filename: :class:`str` | :class:`PathLike`
		:param mode: set to 1 to unzip stable release archive, or 2 to unzip dev-build archive.
		:type mode: :class:`int`
		:return: downloaded/extracted patch files.
		:rtype: `None`
		"""

        logger_stream.info('>> Unzipping patch files...')

        try:
            if mode == 1:  # Unzip stable-release patch files
                with ZipFile(filename) as archive:
                    archive.extractall(path='./patch-files/stable')

                # Remove unnecessary files
                os.unlink('./patch-files/stable/doorstop_config.ini')
                os.unlink(
                    f'./patch-files/stable/BepInEx_stable_{VBPatcher.appglobals.globals.b_stable}.zip'
                )

            elif mode == 2:  # Unzip dev-build patch files
                with ZipFile(filename) as archive:
                    archive.extractall(path='./patch-files/development')
                # Remove unnecessary files
                os.unlink('./patch-files/development/doorstop_config.ini')
                os.unlink(
                    f'./patch-files/development/BepInEx_dev_{VBPatcher.appglobals.globals.b_dev}.zip'
                )

            logger_stream.info(
                '>> Successfully unzipped archive!\n\n>> Deleted extra files...\n>> Patch ready for deployment!\n'
            )

        except Exception as err:
            logger_stream.error(
                f'Encountered error while attempting to unzip archive...\n\n>> Exception: {err}\n'
            )

    def UpdatePatcher(self) -> None:
        """Retrieve latest available patch files.

		---

		:return: download most recent release/build patch files.
		:rtype: `None`
		"""

        # Retrieve latest stable release patch files from http://api.github.com/repos/BepInEx/BepInEx/releases/latest
        if self._dl_stable(VBPatcher.appglobals.globals.url_stable):
            self._unzip_patch(
                f'./patch-files/stable/BepInEx_stable_{VBPatcher.appglobals.globals.b_stable}.zip',
                1)

        # Retrieve development build patch files from https://builds.bepinex.dev/projects/bepinex_be
        if self._dl_dev(VBPatcher.appglobals.globals.url_dev):
            self._unzip_patch(
                f'./patch-files/development/BepInEx_dev_{VBPatcher.appglobals.globals.b_dev}.zip',
                2)

        logger_stream.info('\n>> Press anything to continue...\n')
        m.getch()  # Wait for user to press any key to continue

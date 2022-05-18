
import msvcrt as m
import os
import sys
from zipfile import ZipFile

import VBPatcher.applogger.applogger
import VBPatcher.globalvars.globalvars
import requests
import tqdm

logger = VBPatcher.applogger.applogger._LogGenerator(VBPatcher.globalvars.globalvars._logFile)
class _Downloader:
    """Wrapper containing patch-file update functionality.

    - Class Methods:
        - `dl_stable(self, url) -> BufferedWriter`
            - Download latest BepInEx stable release.
        - `dl_dev(self, url) -> BufferedWriter`
            - Download latest BepInEx development build.
        - `unzip_patch(self, filename, stable) -> None`
            - Unzip downloaded patch files before deleting patch `.zip` archive.
        - `_UpdatePatcher(self) -> None`
            - Process to retrieve latest available patch files using class methods.
    """
    def __init__(self) -> None:
        pass

    def dl_stable(self, url):
        """Download zip containing latest BepInEx stable release.

        :return: zip archive containing patch files.
        :rtype: BufferedWriter
        """

        while True:
            try:
                logger.info('Downloading latest BepInEx stable release...')
                rq = requests.get(url, allow_redirects=True, stream=True)
                file_size = int(rq.headers.get('Content-Length'))
                chunk_size = 1024  # 1 MB
                num_bars = file_size // chunk_size
                with open(f'./patch-files/stable/BepInEx_stable_{VBPatcher.globalvars.globalvars.b_stable}.zip', 'wb') as patch_stable:
                    for chunk in tqdm.tqdm(rq.iter_content(chunk_size=chunk_size), total=num_bars, unit='KB', desc='Downloading Stable Release', file=sys.stdout):
                        patch_stable.write(chunk)
                    logger.info(f'Completed BepInEx latest stable-release download!\n>> Downloaded from url:\n>> {url}\n')
                    print(f'\nCompleted BepInEx latest stable-release download!\n>> Downloaded from url:\n>> {url}\n')
                return patch_stable

            except Exception as err:
                logger.error(f'Encountered error while downloading latest stable release zip archive...\n>> Exception: {err}\n')
                print(f'Encountered error while downloading latest stable release zip archive...\n>> Exception: {err}\n')

                logger.info('Displaying retry update-check prompt...')
                again = input('\nTry again? [y/n]:\n>> ')
                match again.lower():
                    case 'y':
                        continue
                    case _:
                        print('\nCancelled update-check.\n')
                        break

    def dl_dev(self, url):
        """Download zip archive containing latest BepInEx development build.

        :return: zip archive containing patch files.
        :rtype: BufferedWriter
        """
        while True:
            try:
                logger.info('Downloading latest BepInEx development-build...')
                rq = requests.get(url, allow_redirects=True, stream=True)
                file_size = int(rq.headers.get('Content-Length'))
                chunk_size = 1024  # 1 MB
                num_bars = file_size // chunk_size
                with open(f'./patch-files/development/BepInEx_dev_{VBPatcher.globalvars.globalvars.b_dev}.zip', 'wb') as patch_dev:
                    for chunk in tqdm.tqdm(rq.iter_content(chunk_size=chunk_size), total=num_bars, unit='KB', desc='Downloading Dev-Build', file=sys.stdout):
                        patch_dev.write(chunk)
                    logger.info(f'Completed BepInEx latest development-build download!\n>> Downloaded from url:\n>> {url}\n')
                    print(f'\nCompleted BepInEx latest development-build download!\n>> Downloaded from url:\n>> {url}\n')
                return patch_dev

            except Exception as err:
                logger.error(f'Encountered error while downloading latest development-build zip archive...\n>> Exception: {err}\n')
                print(f'Encountered error while downloading latest development-build zip archive...\n>> Exception: {err}')

                logger.info('Displaying retry update-check prompt...')
                again = input('\nTry again? [y/n]:\n>> ')
                match again.lower():
                    case 'y':
                        continue
                    case _:
                        print('\nCancelled update-check.\n')
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
                os.unlink(f'./patch-files/stable/BepInEx_stable_{VBPatcher.globalvars.globalvars.b_stable}.zip')
            else:
                with ZipFile(filename) as archive:
                    archive.extractall(path='./patch-files/development')
                os.unlink('./patch-files/development/doorstop_config.ini')
                os.unlink(f'./patch-files/development/BepInEx_dev_{VBPatcher.globalvars.globalvars.b_dev}.zip')

            logger.info('Successfully unzipped archive!\n>> Deleted extra files...\n>> Patch ready for deployment!\n')
            print('\nSuccessfully unzipped archive!\n>> Deleted extra files...\n>> Patch ready for deployment!\n')

        except Exception as err:
            logger.error(f'Encountered error while attempting to unzip archive...\n>> Exception: {err}\n')
            print(f'\nEncountered error while attempting to unzip archive...\n>> Exception: {err}\n')

    def _UpdatePatcher(self) -> None:
        """Process to retrieve latest available patch files using class methods.

        ---

        :return: most recent release/build patch files.
        :rtype: None
        """
        self.dl_stable(VBPatcher.globalvars.globalvars.url_stable)
        self._unzip_patch(f'./patch-files/stable/BepInEx_stable_{VBPatcher.globalvars.globalvars.b_stable}.zip', True)
        self.dl_dev(VBPatcher.globalvars.globalvars.url_dev)
        self._unzip_patch(f'./patch-files/development/BepInEx_dev_{VBPatcher.globalvars.globalvars.b_dev}.zip', False)

        logger.info('Completed Patcher Update!\n>> Patches ready for deployment!\n')
        print('\nCompleted Patcher Update!\n>> Patches ready for deployment!\n')
        print('Press anything to continue...')
        m.getch()

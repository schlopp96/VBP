#!/usr/bin/env python3
#@ ====================================================================================================== @#
#> Valheim BepInEx Patcher <#
#< Est. 10/24/21 >#
#@ ====================================================================================================== @#
#$ ====================================================================================================== $#
import logging
from os import chdir
from os.path import dirname
from shutil import copytree
from subprocess import call
from sys import exit as ex
from time import sleep
from typing import Any, NoReturn

from PyLoadBar import load

#@ Declare variables containing patch files directory and destination:
chdir(dirname(__file__))
patch_stable: str = './patch-files/stable'
patch_latest: str = './patch-files/bleeding-edge'
build_Stable: str = 'v5.19.00'
build_BleedingEdge: str = 'b50a18a'
patchDestination: str = 'C:\Program Files (x86)\Steam\steamapps\common\Valheim'
textborder: str = "=".ljust((50),"=")
logFile: str = './logs/logfile.log'
__version__: str = 'v0.3.0'

#* Establish Logger:
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler(logFile)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)

#$ ====================================================================================================== $#


def main() -> None | NoReturn:
    """Patcher for BepInEx, a modding console for Valheim.

    - User may choose between several patch installion options:
        - Latest stable build.
        - Latest bleeding-edge (beta) build.
        - Latest stable build, then latest bleeding-edge build afterwards.

    :return: patch BepInEx to chosen build.
    :rtype: None | NoReturn
    """
    logger.debug(f'Welcome to the Valheim Bepinex Patcher {__version__}!\n\n')
    while True:
        choosePatch: str = input(
            f"Welcome to the Valheim Bepinex Patcher!\n\nWhich patch build would you like to install?\n\n{textborder}\n[1.] Stable Release: {build_Stable}\n[2.] Bleeding-Edge Build: {build_BleedingEdge}\n[3.] Full Upgrade (apply both MAIN & BLEEDING-EDGE patches in order of release): {build_Stable} then {build_BleedingEdge}\n[4.] Open Valheim\n[5.] Exit Program\n\n> "
        )
        match choosePatch:
            case '1': stable_patch()
            case '2': BE_patch()
            case '3': full_patch()
            case '4': openValheim()
            case '5':
                logger.info('BepInEx patching process cancelled...\n')
                print('\nBepInEx patching process cancelled...')
                sleep(0.5)
                return exitPatcher()
            case _:
                logger.warning(f'Invalid Input: "{choosePatch}"\n==> Must ONLY enter [1] for stable release {build_Stable}, [2] for bleeding-edge build {build_BleedingEdge}, [3] for FULL upgrade (apply both patches in order), or [4] to exit program <==\n')
                print(f'\n\t- ERROR: Invalid Input -\n\nYour Entry:  "{choosePatch}".')
                sleep(0.750)
                print(
                    f'\n==> Must ONLY enter [1] for stable release {build_Stable}, [2] for bleeding-edge build {build_BleedingEdge}, [3] for FULL upgrade (apply both patches in order), or [4] to exit program <==\n\n'
                )
                sleep(1.250)
                continue

        return exitPatcher()


def stable_patch() -> None:
    """Install latest BepInEx stable-build patch version to local directory.

    :return: Installs BepInEx patch.
    :rtype: None
    """

    while True:
        confirmStable: str = input(
            f'\nReally patch BepInEx to latest stable-build v{build_Stable} in location:\n\n====> "{patchDestination}"?\n\n> Enter [y] or [n]:\n{textborder}\n> '
        )
        match confirmStable.lower():
            case 'yes'|'y':
                patch(patch_stable, patchDestination, build_Stable)
                promptStart()
            case 'n'|'no':
                logger.info('\nBepInEx patching process cancelled.\n')
                with open(logFile, 'a') as fh:
                    fh.write(f'{textborder}\n\n')
                load('\nBepInEx patching process cancelled', '\nClosing window...',
                False)
                break
            case _:
                logger.warning(f'Invalid Input: "{confirmStable}"\n==> Must ONLY enter either [y] for "YES" or [n] for "NO" <==\n')
                print(f'\n\t- ERROR: Invalid Input\n\nYour Entry: "{confirmStable}".')
                sleep(0.750)
                print(
                    '\n==> Must ONLY enter either [y] for "YES" or [n] for "NO" <==\n\n'
                )
                sleep(1.250)
                continue


def BE_patch() -> None:
    """Install latest BepInEx bleeding-edge patch version to local directory.

    :return: Install bleeding-edge patch to BepInEx directory.
    :rtype: None
    """
    while True:
        confirmLatest: str = input(
            f'\nReally patch BepInEx to the latest bleeding-edge beta build {build_BleedingEdge} in location:\n\n====> "{patchDestination}"?\n\n> Enter [y] or [n]:\n{textborder}\n> '
        )
        match confirmLatest.lower():
            case 'yes'|'y':
                patch(patch_stable, patchDestination, build_BleedingEdge)
                promptStart()
            case 'n'|'no':
                logger.info('\nBepInEx patching process cancelled...\n')
                load('\nBepInEx patching process cancelled', '\nClosing window...',
                False)
                break
            case _:
                logger.warning(f'Invalid Input: "{confirmLatest}"\n==> Must ONLY enter either [y] for "YES" or [n] for "NO" <==\n')
                print(f'\n\t- ERROR: Invalid Input -\n\nYour Entry: "{confirmLatest}".')
                sleep(0.750)
                print(
                    '\n==> Must ONLY enter either [y] for "YES" or [n] for "NO" <==\n\n'
                )
                sleep(1.250)
                continue


def full_patch() -> None | bool:
    """Install both latest BepInEx stable patch, before then installing bleeding-edge beta patch.

    :return: Install both stable and bleeding edge patch builds in order of release to BepInEx directory.
    :rtype: None
    """
    while True:
        confirmFull: str = input(
            f'\nReally install latest stable patch {build_Stable} then apply latest "bleeding-edge" build {build_BleedingEdge}?\n> Enter [y] or [n]:\n{textborder}\n> '
        )
        match confirmFull.lower():
            case 'yes'|'y':
                patch(patch_stable, patchDestination, build_Stable)
                patch(patch_stable, patchDestination, build_BleedingEdge)
                return promptStart()
            case 'n'|'no':
                logger.info('\nBepInEx patching process cancelled...\n')
                with open(logFile, 'a') as fh:
                    fh.write(f'{textborder}\n\n')
                return load('\nBepInEx patching process cancelled', '\nClosing window...', enable_display=False)
            case _:
                logger.warning(f'Invalid Input: "{confirmFull}"\n\n==> Must ONLY enter either [y] for "YES" or [n] for "NO" <==\n')
                print(f'\n\t- ERROR: Invalid Input -\n\nYour Entry: "{confirmFull}".')
                sleep(0.750)
                print(
                    '\n==> Must ONLY enter either [y] for "YES" or [n] for "NO" <==\n\n'
                )
                sleep(1.250)
                continue


def promptStart() -> NoReturn | None:
    """Prompt user to choose whether or not to start the game post patching.

    :return: Exits program or starts game.
    :rtype: NoReturn | None
    """
    while True:
        startPrompt: str = input(
            f'\nStart Game?\n\n> Enter [y] or [n]:\n{"=".ljust(16, "=")}\n> ')
        match startPrompt.lower():
            case 'y'|'yes':
                openValheim()
                return exitPatcher()
            case 'n'|'no':
                logger.info('Patching process successfully completed...\n')
                load('\nPatching process successfully completed',
                     '\nClosing window...', enable_display=False)
                return exitPatcher()
            case _:
                logger.warning(f'Invalid Input: "{startPrompt}"\n==> Must ONLY enter either [y] for "YES" or [n] for "NO" <==\n')
                print(f'\n\t- ERROR: Invalid Input -\n\nYour Entry: "{startPrompt}".')
                sleep(0.750)
                print(
                    '\n==> Must ONLY enter either [y] for "YES" or [n] for "NO" <==\n\n'
                )
                sleep(1.250)
                continue


def openValheim() -> int:
    """Calls command to open "Valheim" within Steam client.

    :return: Starts game.
    :rtype: int
    """
    logger.info('Starting Valheim...\n\n')
    load("\nStarting Game", "Opening Valheim...")
    return call(r"C:\Program Files (x86)\Steam\Steam.exe -applaunch 892970")


def patch(patchFile: Any, patchLocation: Any, patchTitle: Any) -> Any:
    """Patch BepInEx according to provided parameter values.

    :param patchFile: Directory containing patch files.
    :type patchFile: Any
    :param patchLocation: Location of BepInEx install directory to install files.
    :type patchLocation: Any
    :param patchTitle: Build title of patch to be installed.
    :type patchTitle: Any
    :return: Patch BepInEx with desired version build.
    :rtype: Any
    """
    logger.info(f'Patching BepInEx build {patchTitle} to location: {patchLocation}...\n\n')
    load(
        f'\nPatching BepInEx build {patchTitle} to location: {patchLocation}',
        f'\nPatch build {patchTitle} successfully installed!')
    logger.info(f'Patch build {patchTitle} successfully installed!\n')
    return copytree(patchFile, patchLocation, dirs_exist_ok=True)


def exitPatcher() -> None | NoReturn:
    logger.info(f'Exiting patcher...\n\n==> End of log...\n{textborder}\n\n')
    return ex()


if __name__ == '__main__':
    main()

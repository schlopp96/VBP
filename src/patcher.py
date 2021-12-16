#!/usr/bin/env python3
#@ ====================================================================================================== @#
#> Valheim BepInEx Patcher <#
#< Est. 10/24/21 >#

#? Why?
#$  - I created this script due to a personal issue I've been having with my modded copy of Valheim;
#!  - BepInEx automatically DOWNGRADES itself upon using the Vortex mod manager.
#*      - This is likely due to Vortex using its own BepInEx downloader, thus overwriting any updated files.
#&          - Has happened to me for BepInEx versions:
#~              1. BepInEx v5.16.0
#>              2. BepInEx v5.17.0
#@ ====================================================================================================== @#
#$ ====================================================================================================== $#
from os import chdir
from os.path import dirname
from shutil import copytree
from subprocess import call
from sys import exit as ex
from time import sleep
from typing import Any, NoReturn

from icecream import ic
from loadingSequence import load
#$ ====================================================================================================== $#

#> Set working directory to folder containing my Python projects.
chdir(dirname(dirname(dirname(__file__))))

textborder: str = '=================================================='


def main() -> None:
    """Patches BepInEx, a modding console for Valheim, to v5.17.00.

    :return: patch BepInEx to v5.17.00
    :rtype: None
    """
    #@ Declare variables containing patch files directory and destination:
    patchContents = "VBP\patch"
    patchDestination = "c:\Program Files (x86)\Steam\steamapps\common\Valheim"

    while True:

        #@ Move BepInEx patch files to Valheim directory:
        confirmation = input(
            f'\nReally patch BepInEx to latest build "30a1089" in location:\n\n====> "{patchDestination}"\n\n> Enter [y] or [n]:\n{textborder}\n> '
        )

        if confirmation.lower() == 'y':

            patch(patchContents, patchDestination)
            promptStart()

        elif confirmation.lower() == 'n':

            load('\nBepInEx patching process cancelled', '\nClosing window...',
                 False)
            break

        else:

            print('\n\t- ERROR: Invalid Input -\n')
            ic(confirmation)
            sleep(0.750)
            print(
                '\n==> Must ONLY enter either [y] for "YES" or [n] for "NO" <==\n\n'
            )
            sleep(1.250)
            continue

    exitPatcher()


def promptStart() -> NoReturn | None:
    while True:
        startPrompt: str = input(
            f"\nStart Game?\n\n> Enter [y] or [n]:\n{textborder}\n> ")

        if startPrompt.lower() == 'y':

            openValheim()
            return ex()

        elif startPrompt.lower() == 'n':

            load('\nPatch successfully completed', '\nClosing window...',
                 False)
            return ex()

        else:

            print('\n\t- ERROR: Invalid Input -\n')
            ic(startPrompt)
            sleep(0.750)
            print(
                '\n==> Must ONLY enter either [y] for "YES" or [n] for "NO" <==\n\n'
            )
            sleep(1.250)
            continue


def openValheim() -> int:
    load("\nStarting Game", "Opening Valheim...")
    return call(r"C:\Program Files (x86)\Steam\Steam.exe -applaunch 892970")


def patch(patch, program) -> Any:
    load(msg_load='\nPatching BepInEx to build 30a1089',
         msg_done='\nPatch successfully installed!')
    return copytree(patch, program, dirs_exist_ok=True)


def exitPatcher() -> NoReturn:
    input('\nPress [ENTER] to exit...')
    ex()


if __name__ == '__main__':
    main()

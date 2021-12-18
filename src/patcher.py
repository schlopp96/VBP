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

#> Set working directory to location containing root VBP repository folder.
chdir(dirname(dirname(dirname(__file__))))

textborder: str = '=================================================='

#@ Declare variables containing patch files directory and destination:
patch_stable = "VBP\patch\stable"
patch_latest = "VBP\patch\latestbuild"
stable_title = "stable build v5.17.00"
latest_title = "bleeding-edge build 30a1089"
patchDestination = "C:\Program Files (x86)\Steam\steamapps\common\Valheim"


def main() -> None:
    """Patches BepInEx, a modding console for Valheim, to v5.17.00.

    :return: patch BepInEx to v5.17.00
    :rtype: None
    """

    while True:
        choosePatch: str = input(
            "Which patch build would you like to install?\n[1.] Stable Build: v5.17.00\n[2.] Bleeding-Edge Build: 30a1089\n\n> "
        )
        if choosePatch == "1":
            while True:
                confirmation: str = input(
                    f'\nReally patch BepInEx to latest STABLE build v5.17.00 in location:\n\n====> "{patchDestination}"?\n\n> Enter [y] or [n]:\n{textborder}\n> '
                )
                if confirmation.lower() in ['y', 'yes']:
                    patch(patch_stable, patchDestination, stable_title)
                    promptStart()
                elif confirmation.lower() in ['n', 'no']:
                    load('\nBepInEx patching process cancelled',
                         '\nClosing window...', False)
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
        elif choosePatch == "2":
            while True:
                confirmation = input(
                    f'\nReally patch BepInEx to latest BLEEDING-EDGE build "30a1089" in location:\n\n====> "{patchDestination}"?\n\n> Enter [y] or [n]:\n{textborder}\n> '
                )
                if confirmation.lower() == 'y':
                    patch(patch_latest, patchDestination, latest_title)
                    promptStart()
                elif confirmation.lower() == 'n':
                    load('\nBepInEx patching process cancelled',
                         '\nClosing window...', False)
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
        else:
            print('\n\t- ERROR: Invalid Input -\n')
            ic(choosePatch)
            sleep(0.750)
            print(
                f'\n==> Must ONLY enter either [1] for {stable_title} or [2] for {latest_title} <==\n\n'
            )
            sleep(1.250)
            continue

        exitPatcher()


def promptStart() -> NoReturn | None:
    while True:
        startPrompt: str = input(
            f"\nStart Game?\n\n> Enter [y] or [n]:\n{textborder}\n> ")

        if startPrompt.lower() in ['y', 'yes']:

            openValheim()
            return ex()

        elif startPrompt.lower() in ['n' 'no']:

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


def patch(patch, program, title) -> Any:
    load(msg_load=f'\nPatching BepInEx to {title}',
         msg_done='\nPatch successfully installed!')
    return copytree(patch, program, dirs_exist_ok=True)


def exitPatcher() -> NoReturn:
    input('\nPress [ENTER] to exit...')
    ex()


if __name__ == '__main__':
    main()

import sys
from subprocess import TimeoutExpired, call
from sys import exit as ex
from time import sleep
from typing import NoReturn

import VBPatcher.appglobals.appglobals
from PyLoadBar import PyLoadBar
from VBPatcher.applogger.applogger import logger, logger_stream

start_seq = PyLoadBar(False)


def _exitPatcher() -> None | NoReturn:
    """Exit the application and finalize log.

    ---

    :return: Exits application.
    :rtype: None | :class:`NoReturn`
    """

    logger.info(
        f'Exiting patcher...\n\n>> End of log...\n\n{VBPatcher.appglobals.appglobals._textborder}\n'
    )
    return ex()


def _openValheim() -> int | None:
    """Calls command to open "Valheim" within Steam client.
    - Will raise :class:`TimeoutExpired` exception if executable doesn't start within 10 seconds.
        - Prevents program from freezing due to any errors encountered during launch process.

    - Steam must be running to properly initialize launch process.

    ---

    :return: Start game client.
    :rtype: :class:`int` | None
    """

    try:
        logger.info('Starting Valheim...\n\n')
        start_seq.start("Starting Game", "Opening Valheim...\n")
        return call(
            r"C:\Program Files (x86)\Steam\Steam.exe -applaunch 892970",
            timeout=15,
            stdout=sys.stdout,
            stderr=sys.stderr)

    except TimeoutExpired as exp:
        logger_stream.error(
            f'Something went wrong while starting Valheim...\n\n>> Exception:\n{exp}\n>> Make sure Steam is running!\n'
        )
        return _exitPatcher()


def _startPrompt() -> NoReturn | None:
    """Prompt user to decide whether to start Valheim immediately after program exit or not.

    ---

    :return: display user prompt.
    :rtype: :class:`NoReturn` | None
    """

    while True:
        logger.info('Displaying start game prompt...')
        startPrompt: str = input(
            f'\nStart Game?\n\n> Enter [y] or [n]:\n{VBPatcher.appglobals.appglobals._textborder}\n> '
        )
        if startPrompt.lower() in {'y', 'yes'}:
            return _openValheim()

        elif startPrompt.lower() in {'n', 'no'}:
            logger.info(
                'Patching process successfully completed!\n>> Preparing to exit...\n'
            )
            start_seq.start('Patching process successfully completed',
                            'Preparing to exit...',
                            iter_total=10,
                            txt_seq_speed=0.25)
            return _exitPatcher()

        else:
            logger_stream.warning(
                f'Invalid Input: "{startPrompt}"\n>> Must ONLY enter either [y] for "YES" or [n] for "NO".\n'
            )
            sleep(1.250)
            continue

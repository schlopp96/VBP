from datetime import datetime

import bs4
import requests as req
from requests import Response


def _get_stable_assets(url: str, mode: int) -> str:
    """Send GET request to retrieve BepInEx stable release assets, depending on value passed to :param:`mode`.

    - If :param:`mode` == `1`, get patch archive download link.
    - If :param:`mode` != `1`, get patch release version number as string.

    ---

    :param url: URL for the new :class:`Request` object.
    :type url: :class:`str` | :class:`PathLike`
    :param mode: specifies values to retrieve from response.
    :type mode: :class:`int`
    :return: response content from GET request.
    :rtype: :class:`str`
    """

    r: Response = req.get(url, 'html.parser')  # Send GET request.
    r.raise_for_status()  # Raise exception if response is not 200.

    dl_link: str = r.json()['assets'][1][
        'browser_download_url']  # Get download link.
    patch_ver: str = r.json()['assets'][1]['name'][12:20]  # Get patch version.

    return dl_link if mode == 1 else patch_ver


def _get_dev_assets(url: str, mode: int) -> str:
    """Send GET request to retrieve BepInEx dev/bleeding-edge release assets, depending on value passed to :param:`mode`.

    - If :param:`mode` == `1`, get patch archive download link.
    - If :param:`mode` != `1`, get patch version number as string.

    ---

    :param url: URL for the new :class:`Request` object.
    :type url: :class:`str` | :class:`PathLike`
    :param mode: specifies values to retrieve from response.
    :type mode: :class:`int`
    :return: response content from GET request.
    :rtype: :class:`str`
    """

    retrieved: int = 0

    r: Response = req.get(url)  # Send GET request.
    r.raise_for_status()  # Raise exception if error code is returned.

    soup = bs4.BeautifulSoup(r.content, 'html.parser')  # Parse response HTML.
    results = soup.find_all(
        'div', class_="artifacts-list"
    )  # Get all <div> tags with class="artifacts-list".

    for result in results:
        if retrieved < 1:  # Only get 2nd <div> tag.
            link = result.find_all('a')[1]['href']  # Get download link.
            retrieved += 1

    dl_link = (f'{url[:26]}{link}')  # Combine URL and download link.

    return dl_link if mode == 1 else dl_link[93:100]


class _Getch:
    """Gets a single character from standard input.  Does not echo to the screen."""

    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self):
        char = self.impl()
        if char == '\x03':
            raise KeyboardInterrupt
        elif char == '\x04':
            raise EOFError
        return char


class _GetchUnix:

    def __init__(self):
        import sys
        import tty

    def __call__(self):
        import sys
        import termios
        import tty
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:

    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


getch = _Getch()

__version__: str = '0.9.0'

p_stable: str = r'.\patch-files\stable'  # Stable patch file location

url_stable: str = _get_stable_assets(
    'http://api.github.com/repos/BepInEx/BepInEx/releases/latest',
    1)  # stable release download link

b_stable: str = _get_stable_assets(
    'http://api.github.com/repos/BepInEx/BepInEx/releases/latest',
    2)  # stable release version

p_dev: str = r'.\patch-files\development'  # Development patch file location

url_dev: str = _get_dev_assets(
    'https://builds.bepinex.dev/projects/bepinex_be',
    1)  # dev/bleeding-edge build download link

b_dev: str = _get_dev_assets('https://builds.bepinex.dev/projects/bepinex_be',
                             2)  # dev/bleeding-edge build number

p_targetDir: str = r'C:\Program Files (x86)\Steam\steamapps\common\Valheim'  # target directory to patch

logFile: str = r'.\logs\VBPatcherLog.log'  # Log file path

datefmt: str = datetime.now().strftime(
    "%Y-%m-%d %H:%M:%S"
)  # Date and time format to display when starting program.

textborder: str = "=".ljust((78),
                            "=")  # Text border for log file organization.

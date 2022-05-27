from datetime import datetime

import requests as req
from requests import Response


def get_stable_assets(url: str, mode: int):
    """If `mode` set to 1, send GET request and retrieve download URL for latest BepInEx release, or retrieve release version if `mode`set to 2.

    ---

    :param url: url to send GET request to.
    :type url: :class:`str` | :class:`PathLike`
    :param mode: specifies whether to retrieve latest release download URL or release version.
    :type mode: :class:`int`
    :return: get download URL for latest BepInEx release if `mode` set to 1, or retrieve latest release version if `mode` set to 2.
    :rtype: :class:`str` | None
    """
    r: Response = req.get(url, 'html.parser')
    r.raise_for_status()
    dl_url: str = r.json()['assets'][1]['browser_download_url']
    dl_ver: str = r.json()['assets'][1]['name'][12:20]
    if mode == 1:
            return dl_url
    if mode == 2:
            return dl_ver


p_stable: str = r'.\patch-files\stable' # Stable patch file path
url_stable = get_stable_assets(
    'http://api.github.com/repos/BepInEx/BepInEx/releases/latest', 1) # stable release download link
b_stable = get_stable_assets(
    'http://api.github.com/repos/BepInEx/BepInEx/releases/latest', 2)  #release version

p_dev: str = r'.\patch-files\development'
url_dev = 'https://builds.bepinex.dev/projects/bepinex_be/562/BepInEx_UnityMono_x64_7a97bdd_6.0.0-be.562.zip'
b_dev: str = url_dev[73:80]  # build number

p_targetDir: str = r'C:\Program Files (x86)\Steam\steamapps\common\Valheim'

_logFile: str = r'.\logs\patchLog.log'

_datefmt: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

_textborder: str = "=".ljust((78), "=")

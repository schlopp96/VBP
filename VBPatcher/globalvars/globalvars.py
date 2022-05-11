from datetime import datetime


p_stable: str = r'.\patch-files\stable'
url_stable = 'https://github.com/BepInEx/BepInEx/releases/download/v5.4.19/BepInEx_x64_5.4.19.0.zip'
b_stable: str = url_stable[53:60]  #release version

p_dev: str = r'.\patch-files\development'
url_dev = 'https://builds.bepinex.dev/projects/bepinex_be/562/BepInEx_UnityMono_x64_7a97bdd_6.0.0-be.562.zip'
b_dev: str = url_dev[73:80]  # build number

p_targetDir: str = r'C:\Program Files (x86)\Steam\steamapps\common\Valheim'

_logFile: str = r'.\logs\patchLog.log'

_datefmt: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

_textborder: str = "=".ljust((61), "=")
# VBPatcher

> Valheim BepInEx Patcher

---

## About

- The Valheim BepInEx Patcher _**(VBPatcher)**_ is a CLI program created to solve the weird automatic version downgrading issue of the BepInEx modding tool while using the Vortex modding tool.

- For me, this is generally caused by the Vortex mod manager automatically downloading what it incorrectly perceives to be the "latest" version of BepInEx.

---

## Installation

### Using PIP _(Recommended)_

- To install VBPatcher using `pip`, enter the following:

  ```python
  pip install VBPatcher
  ```

### Manual Installation _(**NOT** Recommended)_

1. Download the project's latest release **.zip archive** from the ["releases"](https://github.com/schlopp96/VBPatcher/releases) tab and extract to location of choice.

2. Open terminal and navigate to the extracted directory `"~/VBPatcher"`.

3. Enter `pip install -r requirements.txt` to install necessary dependencies.

---

## Usage

- Make sure you **do not** have Vortex, Thunderstore, or any other modding tools running, and that you are done with any modding processes.

- Each time your modding tool is opened to edit Valheim, your files will be downgraded again, so **I highly recommend running this script every time before playing!**

1. Open the script, which can be found inside the downloaded folder here: `~/VBPatcher/main.py`.

2. Once the script is run, you will be prompted to choose whether to install the latest available build, the latest available stable version of BepInEx patch, or _both_ to ensure the latest possible build available. You may also choose to check for new BepInEx patch releases.

3. Once an option is chosen, you will then be asked to confirm that the correct option/location is chosen.

4. For example, once the option to apply a patch is confirmed, the script will begin patching the appropriate files immediately, and should finish in seconds.

5. Upon successful patching, the script will ask the user if they'd like to open the game, or simply exit the patcher.

6. If you choose to run the game, the patcher will automatically close itself after running the game's executable.

7. If you choose to NOT run the game, the patcher will then close itself.

- Works with both Vulkan and the default graphics API.

- **_NOTE:_**

  - As of now, BepInEx will _still_ list its current version as the last stable build number, even if a "Development Build" patch is installed. It will still work all the same.

  - If you wish to verify, you can either compare the files contained in the patch to the ones you have on your machine using a diff tool, or simply side-to-side by eye.

  - **_Note that you can also find the latest bleeding-edge-builds of BepInEx [here](https://builds.bepis.io/projects/bepinex_be)._**

### Opening VBPatcher

---

- Within a python environment, open VBPatcher with:

  ```python
  >>> import VBPatcher # Import package
  >>> VBPatcher.vbp()  # Call method to open program

  ```

- Or optionally:

  ```python
    >>> from VBPatcher import vbp
    >>> vbp()
  ```

- Example output from VBPatcher installing the stable version of BepInEx before installing the latest experimental patch build [Option 3 in the program]:

  ```python
  Welcome to the Valheim Bepinex Patcher!
  Please Choose an Option by Entering its Corresponding Number:

  =============================================================
  >> [1] Patch BepInEx to latest stable release: v5.19.00 (2/3/22)
  >> [2] Patch BepInEx to latest development/expiremental build: da48b77 (4/21/22)
  >> [3] Apply both patches to BepInEx in chronological order of release (v5.19.00 then da48b77)
  >> [4] Check for updates to newest patch versions
  >> [5] Open Valheim
  >> [6] Exit Program

  > 3

  Really apply both latest stable release v5.19.00, and latest development build da48b77?
  > Enter [y] or [n]:
  =============================================================
  > y

  Patching BepInEx build v5.19.00 to location: C:\Program Files (x86)\Steam\steamapps\common\Valheim...

  100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 5/5 [00:00<00:00,  9.14it/s]


  Patch build v5.19.00 successfully installed!

  Patching BepInEx build da48b77 to location: C:\Program Files (x86)\Steam\steamapps\common\Valheim...

  100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 5/5 [00:00<00:00,  9.19it/s]


  Patch build da48b77 successfully installed!

  Start Game?

  > Enter [y] or [n]:
  =============================================================
  > n

  Patching process successfully completed.....


  Preparing to exit...
  ```

---
---

## How It Works

- The script simply copies the relevant patch files & places/overwrites core files responsible for the BepInEx version downgrade.

- The patch files will all be placed in either one of two potential locations within Valheim's install directory

- The location of the game's install directory is different depending on the operating system of the user.

  - For _Windows_, the default install path for Valheim is:

    - `C:\Program Files (x86)\Steam\steamapps\common\Valheim`

  - For _MacOS_, the default install path for Valheim is:
    - `~/Library/Application Support/Steam/steamapps/common/Valheim`

- Patches will be applied to the BepInEx folder, itself found within the game's installation folder: `~/Steam/steamapps/common/Valheim/BepInEx`.

---

## Contact the Author

- If you have any questions, comments, issues, complaints, etc, feel free to contact me through my:
  - Email at: `schloppdaddy@gmail.com`.
  - Submit an issue on the project's [GitHub repository](https://github.com/schlopp96/VBPatcher)

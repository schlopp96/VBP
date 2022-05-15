# VBPatcher

> Valheim BepInEx Patcher

---

## About

- **V**alheim **B**epInEx **P**atcher is a CLI application for patching the Unity modding plugin, [_**BepInEx**_](https://github.com/BepInEx/BepInEx) to its latest release (whether LTS or experimental).

- **VBP** was originally created as a solution for an issue that occurs while using the [**_Vortex_**](https://) modding tool to mod the game **Valheim**, whilst having **BepInEx** installed.

  - When opening **Vortex** to begin modding Valheim, the modding tool automatically downloads what it _incorrectly_ perceives to be the "latest" version of **BepInEx** (a necessary requirement for the vast majority of mods available) which is generally incorrect, and often takes a long time to be fixed.

  - Unfortunately, this means if you were using an experimental/newer/different build of **BepInEx**, it has been overwritten by whatever build **Vortex** installed.

  - This occurs _each and every time_ you open **Vortex**, and became a major annoyance for me, so I decided to create a quick solution to make this problem less annoying.

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

- Make sure you **do not** have **Vortex**, **Thunderstore**, or any other modding tools running, and that you are done with any modding processes.

- Each time your modding tool is opened to edit Valheim, your files will be downgraded again, so **I highly recommend running this script every time before playing!**

1. Open the application, which can be run within a terminal using the following command:

   - **`> start_vbp`**
   - You can also run **VBP** from the main program file:
     - `~/VBPatcher/main.py`.

2. Once the script is run, you will be presented with an option menu, allowing you to choose whether to:

   - Patch **BepInEx** to the latest developmental/experimental "bleeding-edge" build
   - Patch **BepInEx** to the latest stable release
   - Patch **BepInEx** first with the latest stable release, and **then** with the latest experimental build to ensure a safe installation
   - Check to ensure required patch-files are present and ready to be deployed (is also done at start of program, but I decided to leave this option in for now)
   - Check for and download new releases/builds of **BepInEx** _**(COMING SOON!)**_

3. Once an option is chosen, you will then be asked to confirm that the correct option/location is chosen.

   - For example, once the option to apply a patch is confirmed, the script will begin patching the appropriate files immediately, and should finish in seconds.

4. Upon successful patching, the script will ask the user if they'd like to start **Valheim**, or simply exit the patcher.

5. If you choose to run the game, the patcher will automatically close itself after running the game's executable.

6. If you choose to **NOT** run the game, the patcher simply closes itself.

- **_NOTE:_**

  - As of now, BepInEx will _still_ list its current version as the last stable build number, even if a "Development Build" patch is installed. It will still work all the same.

  - If you wish to verify, you can either compare the files contained in the patch to the ones you have on your machine using a diff tool, or simply side-to-side by eye.

  - **_Note that you can also find the latest bleeding-edge-builds of BepInEx [here](https://builds.bepis.io/projects/bepinex_be)._**

---

### How It Works

- **VBP** functions by simply copying the relevant patch files & places/overwrites core files responsible for the BepInEx version downgrade.

- The patch files will all be placed in either one of two potential locations within Valheim's install directory

- The location of the game's install directory is different depending on the operating system of the user.

  - For _Windows_, the default install path for Valheim is:

    - `C:\Program Files (x86)\Steam\steamapps\common\Valheim`

  - For _MacOS_, the default install path for Valheim is:
    - `~/Library/Application Support/Steam/steamapps/common/Valheim`

- Patches will be applied to the BepInEx folder, itself found within the game's installation folder:
  - `~/Steam/steamapps/common/Valheim/BepInEx`.

---

### Opening VBPatcher

- Within a terminal, open **VBP** with the following command:

  ```text
  > start_vbp
  ```

- Or optionally within a python environment:

  ```python
  >>> import VBPatcher # Import package
  >>> VBPatcher.vbp()  # Call method to open program

  ```

  ```python
    >>> from VBPatcher import vbp # Import package
    >>> vbp() # Call method to open program
  ```

- Example output from VBPatcher installing the stable version of BepInEx before installing the latest experimental patch build [option 3 in the program]:

  ```python
  Welcome to the Valheim Bepinex Patcher!
  Please Choose an Option by Entering its Corresponding Number:

  =============================================================
  >> [1] Patch BepInEx to latest stable release: v5.19.00 (2/3/22)
  >> [2] Patch BepInEx to latest development/expiremental build: 7a97bdd (5/7/22)
  >> [3] Apply both patches to BepInEx in chronological order of release (v5.19.00 then 7a97bdd)
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

## Contact the Author

- If you have any questions, comments, issues, complaints, etc, feel free to contact me through my:
  - Email at: `schloppdaddy@gmail.com`.
  - Submit an issue on the project's [GitHub repository](https://github.com/schlopp96/VBPatcher)

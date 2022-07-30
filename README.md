# VBPatcher

> Valheim BepInEx Patcher

---

## About

- _**V**alheim **B**epInEx **P**atcher_ (_**VBP**_) is a CLI application for patching the Unity modding plugin, [_**BepInEx**_](https://github.com/BepInEx/BepInEx), to its latest release (whether LTS or experimental).

- _**VBP**_ was originally created as a solution for an issue that occurs while using the [**_Vortex_**](https://www.nexusmods.com/site/mods/1) modding tool to mod the game _**Valheim**_, whilst having _**BepInEx**_ installed.

  - When opening **_Vortex_** to begin modding **_Valheim_**, the modding tool automatically downloads what it _incorrectly_ perceives to be the "latest" version of _**BepInEx**_ (a necessary requirement for the vast majority of mods available) which is generally incorrect, and often takes a long time to be fixed.

  - Unfortunately, this means if you were using an experimental/newer/different build of _**BepInEx**_, it has been overwritten by whatever build _**Vortex**_ installed.

  - This occurs _each and every time_ you open _**Vortex**_, and became a major annoyance for me, so I decided to create a quick solution to make this problem less annoying.

---

## Installation

### **Using PIP** _(Recommended)_

- To install _**VBP**_ using `pip`, enter the following:

  - ```shell
      python -m pip install VBPatcher
    ```

- Done!

### **Manual Installation** _(**NOT** Recommended)_

1. Download the project's latest release **\*.zip archive** from the ["releases"](https://github.com/schlopp96/VBPatcher/releases) tab and extract to location of choice, or clone repository with the git client of your preference with:

   - ```shell
      gh repo clone schlopp96/VBPatcher
     ```

2. Open terminal and navigate to the extracted directory `"~/VBPatcher"`.

3. Enter the following to install necessary dependencies:

   - ```shell
      pip install -r requirements.txt
     ```

- Done!

---

## Usage

- Make sure you **do not** have **Vortex**, **Thunderstore**, or any other modding tools running, and that you are done with any modding processes.

- Each time Vortex is opened to mod Valheim, your BepInEx version will be downgraded again, so **I highly recommend running this script every time before playing!**

1. Open the application, which can be run within a terminal using the following command:

   - ```shell
     vbpatcher
     ```

   - You can also run **VBPatcher** from the main program file:
     - `~/VBPatcher/main.py`.

2. Once the script is run, you will be presented with an option menu, allowing you to choose from the following commands:

   - Patch BepInEx to the latest stable release.
   - Patch BepInEx to the latest developmental/experimental "bleeding-edge" build.
   - Patch BepInEx first with the latest stable release, and **then** with the latest experimental build to ensure a safe installation.
   - Check for and download new releases/builds of BepInEx.
   - Start Valheim.
   - Exit the application.

3. Once an option is chosen, you will then be asked to confirm that the correct option/location is chosen.

   - For example, once the option to apply a patch is confirmed, the script will begin patching the appropriate files immediately, and should finish in seconds.

4. Upon successful patching, the script will ask the user if they'd like to start _Valheim_, or simply exit the patcher.

5. If you choose to run the game, the patcher will automatically close itself after running the game's executable.

6. If you choose to **NOT** run the game, the patcher simply closes itself.

- **_NOTE:_**

  - BepInEx will list its current version as the last stable build number, even if a bleeding-edge build is installed. It will still work all the same.

  - If you wish to verify, you can either compare the files contained in the patch to the ones you have on your machine using a diff tool, or simply side-to-side by eye.

  - **_Note that you can also find the latest bleeding-edge-builds of BepInEx [here](https://builds.bepis.io/projects/bepinex_be)._**

---

### How It Works

- **VBPatcher** functions by simply copying the relevant patch files & places/overwrites core files responsible for the BepInEx version downgrade.

- The patch files will all be placed in either one of two potential locations within Valheim's install directory

- The location of the game's install directory is different depending on the operating system of the user.

  - For _Windows_, the default install path for Valheim is:

    - `C:\Program Files (x86)\Steam\steamapps\common\Valheim`

  - For _MacOS_, the default install path for Valheim is:
    - `~/Library/Application Support/Steam/steamapps/common/Valheim`

- Patches will be applied to the BepInEx folder, itself found within the game's installation folder:
  - `~/Steam/steamapps/common/Valheim/BepInEx`.

---

### Opening **VBPatcher**

- Within a terminal, open **VBP** with the following command:

  ```shell
    vbpatcher
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

- From here, follow the on-screen prompts to operate the program.
- Choose an operation to run by entering the corresponding number (1-6) and pressing enter.

---

## Usage Example

- The following depicts the output from using **VBPatcher** from a command line to first check for any new updates before installing the latest base/stable-release of BepInEx, then the newest dev-build/bleeding-edge patch [option 3 in the program]:

![alt](./assets/README-GIF.gif)

---

## Contact

- If you have any questions, comments, issues, complaints, etc, feel free to:
  - contact me through my email at: `schloppdaddy@gmail.com`.
  - Submit an issue to the project's [GitHub repository](https://github.com/schlopp96/VBPatcher)

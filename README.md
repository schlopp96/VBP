# VBP

> Valheim BepInEx Patcher

---

## About

- The Valheim BepInEx Patcher _**(VBP)**_ is a personal script created to solve the weird automatic version downgrading of the BepInEx modding tool.

- For me, this is generally caused by the Vortex mod manager automatically downloading what it perceives to be the "necessary" files for modding.

---

## How to Use the Script

- Make sure you **do not** have Vortex, Thunderstore, or any other modding tools running, and that you are done with any modding processes.

- Each time your modding tool is opened to edit Valheim, your files will be downgraded again, so **you must run this script every time before playing!**

1. Open the script, which can be found inside the downloaded folder here: "VBP/src/patcher.py".

2. Once the script is run, you will be prompted to choose whether to install the latest available build, the latest available stable version of BepInEx patch, or *both* to ensure the latest possible build available.

3. Once chosen, you will then be asked to confirm that the correct option/location is chosen.

4. Once confirmed, the script will begin patching the appropriate files immediately, and should finish in seconds.

5. Upon successful patching, the script will ask the user if they'd like to open the game, or simply exit the patcher.

6. If you choose to run the game, the patcher will automatically close itself after running the game's executable.

7. If you choose to NOT run the game, the patcher will prepare itself to close, and will penultimately prompt you to press [ENTER] to exit the application/close the console window.

- Works with both Vulkan and the default graphics API.

- NOTE: As of now, BepInEx will _still_ list its current version as the last stable build number, even if a "Bleeding-Edge Build" patch is installed. It will still work all the same.

  - If you wish to verify, you can either compare the files contained in the patch to the ones you have on your machine using a diff tool, or simply side-to-side by eye.

- ***Note that you can also find the latest bleeding-edge-builds of _BepInEx_ [here](https://builds.bepis.io/projects/bepinex_be).***

---

## How It Works

- The script simply copies the included patch files & places/overwrites matching core files responsible for the BepInEx version downgrade.

- The patch files will all be placed in either one of two potential locations within Valheim's install directory

- The location of the game's install directory is different depending on the operating system of the user.

  - For _Windows_, the default install path for Valheim is:

    - `C:\Program Files (x86)\Steam\steamapps\common\Valheim`

  - On Mac, the default install path for Valheim is:
    - `~/Library/Application Support/Steam/steamapps/common/Valheim`

- One file, "./patch/stable/winhttp.dll", will be copied directly inside the installation folder: "install_location/Valheim".

- The rest will be copied within the BepInEx folder, itself found within the game's installation folder: "install_location/Valheim/BepInEx/core".

---

## Contact the Author

- If you have any questions, comments, issues, complaints, etc, feel free to contact me through my email at: `schloppdaddy@gmail.com`

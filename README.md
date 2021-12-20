# VBP

> Valheim BepInEx Patcher

## About

- The Valheim BepInEx Patcher _**(VBP)**_ is a personal script created to solve the weird automatic version downgrading of the BepInEx modding tool.

- For me, this is generally caused by the Vortex mod manager automatically downloading what it perceives to be the "necessary" files for modding.

---

## How to Use the Script

- Make sure you **do not** have Vortex, Thunderstore, or any other modding tools running, and that you are done with any modding processes.

- Each time your modding tool is opened to edit Valheim, your files will be downgraded again, so **you must run this script every time before playing!**

1. Open the script, which can be found inside the downloaded folder here: "VBP/src/patcher.py".

2. Once the script is run, you will be prompted to choose whether to install the latest available build, or the latest available stable version of BepInEx patch.

3. Once chosen, you will then be asked to confirm that the correct option/location is chosen.

4. Once confirmed, the script will begin patching the appropriate files immediately, and should finish in seconds.

5. Upon successful patching, the script will ask the user if they'd like to open the game, or simply exit the patcher.

6. If you choose to run the game, the patcher will automatically close itself after running the game's executable.

7. If you choose to NOT run the game, the patcher will prepare itself to close, and will penultimately prompt you to press [ENTER] to exit the application/close the console window.

- Works with both Vulkan and the default graphics API.

- If BepInEx lists its current version as v5.17.00, then it worked for either build!

---

## How It Works

- The script simply copies the included patch files & places/overwrites matching core files responsible for the BepInEx version downgrade.

- The patch files will all be placed in either one of two potential locations within Valheim's install directory

- The location of the game's install directory is different depending on the operating system of the user.

  - For _Windows_, the default install path for Valheim is:

    - `C:\Program Files (x86)\Steam\steamapps\common\Valheim`

  - On Mac, the default install path for Valheim is:
    - `~/Library/Application Support/Steam/steamapps/common/Valheim`

- One file, "./patch/winhttp.dll", will be copied directly inside the installation folder: "install_location/Valheim".

- The rest will be copied within the BepInEx folder, itself found within the game's installation folder: "install_location/Valheim/BepInEx/core".

---

## Files Included in Patch

- Patch file intended for the game's root install directory (contains BepInEx folder where all other files will go):

  - "./patch/winhttp.dll"

- Patch files that will replace necessary core files (from within the BepInEx directory which itself):

  - "./patch/BepInEx/core/0Harmony.dll"

  - "./patch/BepInEx/core/BepInEx.Core.dll"

  - "./patch/BepInEx/core/BepInEx.Core.xml"

  - "./patch/BepInEx/core/BepInEx.Preloader.Core.dll"

  - "./patch/BepInEx/core/BepInEx.Preloader.Core.xml"

  - "./patch/BepInEx/core/BepInEx.Preloader.Unity.dll"

  - "./patch/BepInEx/core/BepInEx.Preloader.Unity.xml"

  - "./patch/BepInEx/core/BepInEx.Unity.dll"

  - "./patch/BepInEx/core/BepInEx.Unity.xml"

  - "./patch/BepInEx/core/SemanticVersioning.dll"

  - "./patch/BepInEx/core/0Harmony.xml"

  - "./patch/BepInEx/core/0Harmony20.dll"

  - "./patch/BepInEx/core/BepInEx.dll"

  - "./patch/BepInEx/core/BepInEx.Harmony.dll"

  - "./patch/BepInEx/core/BepInEx.Harmony.xml"

  - "./patch/BepInEx/core/BepInEx.Preloader.dll"

  - "./patch/BepInEx/core/BepInEx.Preloader.xml"

  - "./patch/BepInEx/core/BepInEx.xml"

  - "./patch/BepInEx/core/HarmonyXInterop.dll"

  - "./patch/BepInEx/core/Mono.Cecil.dll"

  - "./patch/BepInEx/core/Mono.Cecil.Mdb.dll"

  - "./patch/BepInEx/core/Mono.Cecil.Pdb.dll"

  - "./patch/BepInEx/core/Mono.Cecil.Rocks.dll"

  - "./patch/BepInEx/core/MonoMod.RuntimeDetour.dll"

  - "./patch/BepInEx/core/MonoMod.RuntimeDetour.xml"

  - "./patch/BepInEx/core/MonoMod.Utils.dll"

  - "./patch/BepInEx/core/MonoMod.Utils.xml"

---

## Contact the Author

- If you have any questions, comments, issues, complaints, etc, feel free to contact me through my listed email on my GitHub profile, or through the discussions page!

from pathlib import Path

import atlas_builder
import lsx_writer

# provide input directory (location of 64x64 icon.png files)
INPUT_PATH = Path("./.icons")
# provide output directory
OUTPUT_PATH = Path("./.out")
# provide a name for your atlas - this should be unique to your mod
ATLAS_NAME = "Icons_MyModAtlas"
# provide your mod's folder name
#   usually ModName_GUID: Mods/{MOD_FOLDER} or Public/{MOD_FOLDER}
MOD_FOLDER = "MyMod_asd448e6e-67d9-4742-9a27-923a3387d923"
# provide a RESOURCE_UUID if you want to overwrite an existing resource
#   otherwise one will be generated for you
RESOURCE_UUID = None


def main() -> None:
    """Build the icon atlas and write corresponding LSX/LSF files."""
    atlas, icon_nodes = atlas_builder.build(
        INPUT_PATH,
        OUTPUT_PATH,
        ATLAS_NAME,
        MOD_FOLDER,
        RESOURCE_UUID,
    )
    lsx_writer.write(atlas, icon_nodes)


if __name__ == "__main__":
    main()

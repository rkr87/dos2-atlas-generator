from pathlib import Path

import atlas_builder
import image_writer
import lsx_writer
from models.resource_details import ResourceDetails

# provide input directory (location of 64x64 icon.png files)
INPUT_PATH = "./.icons"
# provide icon size
#   all provided icons should match this value for both width and height
ICON_SIZE = 64
# provide output directory
OUTPUT_PATH = "./.out"
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
    atlas, image, icon_nodes = atlas_builder.build(
        Path(INPUT_PATH),
        ICON_SIZE,
    )
    resource_details = ResourceDetails.new(
        Path(OUTPUT_PATH), ATLAS_NAME, RESOURCE_UUID, MOD_FOLDER
    )
    image_writer.write(image, resource_details)
    lsx_writer.write(atlas, icon_nodes, resource_details)


if __name__ == "__main__":
    main()

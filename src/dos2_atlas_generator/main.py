from pathlib import Path

import atlas_builder
import image_writer
import lsx_writer
from models.resource_details import ResourceDetails

# provide input directory (location of 64x64 icon.png files)
INPUT = "./.icons"
# provide icon size
#   all provided icons should match this value for both width and height
ICON_SIZE = 64
# provide output directory
OUTPUT = "./.out"
# provide a name for your atlas - this should be unique to your mod
NAME = "Icons_MyModAtlas"
# provide your mod's folder name
#   usually ModName_GUID: Mods/{MOD_FOLDER} or Public/{MOD_FOLDER}
MOD_DIR = "MyMod_asd448e6e-67d9-4742-9a27-923a3387d923"
# provide a RESOURCE_UUID if you want to overwrite an existing resource
#   otherwise one will be generated for you
RESOURCE_UUID = None


def main() -> None:
    """Build the icon atlas and write corresponding LSX/LSF files."""
    atlas, image, nodes = atlas_builder.build(Path(INPUT), ICON_SIZE)
    res_det = ResourceDetails.new(Path(OUTPUT), NAME, RESOURCE_UUID, MOD_DIR)
    image_writer.write(image, res_det)
    lsx_writer.write(atlas, nodes, res_det)


if __name__ == "__main__":
    main()

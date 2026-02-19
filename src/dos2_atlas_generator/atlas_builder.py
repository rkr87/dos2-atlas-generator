from pathlib import Path

from converter import dds
from models.atlas import Atlas
from models.icon_node import IconNode
from PIL import Image

_ICON_FILE_TYPE = ".png"


def _get_icons(input_path: Path) -> list[Path]:
    return [
        icon_path
        for icon_path in input_path.iterdir()
        if icon_path.suffix.lower() == _ICON_FILE_TYPE
    ]


def _generate_atlas_image(
    icon_paths: list[Path], atlas: Atlas
) -> tuple[Image.Image, list[IconNode]]:
    atlas_image = Image.new("RGBA", (atlas.layout.size, atlas.layout.size))
    icon_nodes: list[IconNode] = []

    for i, icon_path in enumerate(icon_paths):
        icon_image = Image.open(icon_path).convert("RGBA")
        node = IconNode.from_index(i, icon_path.stem, atlas)
        atlas_image.paste(
            icon_image,
            (node.x * atlas.cell.icon_size, node.y * atlas.cell.icon_size),
        )
        icon_nodes.append(node)

    return atlas_image, icon_nodes


def _write_image_files(atlas: Atlas, atlas_image: Image.Image) -> None:
    atlas_image.save(atlas.path.image, compress_level=0, icc_profile=None)
    dds.from_png(atlas.path.image)


def build(
    input_path: Path,
    output_path: Path,
    atlas_name: str,
    mod_folder: str,
    resource_uuid: str | None,
) -> tuple[Atlas, list[IconNode]]:
    """Build an icon atlas and return its detail and IconNodes."""
    icon_paths = _get_icons(input_path)
    atlas = Atlas.from_icon_count(
        len(icon_paths), atlas_name, output_path, mod_folder, resource_uuid
    )
    atlas_image, icon_nodes = _generate_atlas_image(icon_paths, atlas)
    _write_image_files(atlas, atlas_image)
    return atlas, icon_nodes

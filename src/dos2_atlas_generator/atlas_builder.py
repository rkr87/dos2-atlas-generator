from pathlib import Path

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
            (node.x * atlas.layout.icon_size, node.y * atlas.layout.icon_size),
        )
        icon_nodes.append(node)

    return atlas_image, icon_nodes


def build(
    input_path: Path, icon_size: int
) -> tuple[Atlas, Image.Image, list[IconNode]]:
    """Build an icon atlas and return its detail and IconNodes."""
    icon_paths = _get_icons(input_path)
    atlas = Atlas.from_icon_count(len(icon_paths), icon_size)
    atlas_image, icon_nodes = _generate_atlas_image(icon_paths, atlas)
    return atlas, atlas_image, icon_nodes

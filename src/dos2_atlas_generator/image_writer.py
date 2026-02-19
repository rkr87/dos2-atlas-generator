from pathlib import Path

from converter import dds
from models.resource_details import ResourceDetails
from PIL import Image


def _write_image_files(image_path: Path, atlas_image: Image.Image) -> None:
    atlas_image.save(image_path, compress_level=0, icc_profile=None)
    dds.from_png(image_path)


def write(
    atlas_image: Image.Image,
    resource_details: ResourceDetails,
) -> None:
    """Write atlas image files using the provided resource details."""
    _write_image_files(resource_details.image_path, atlas_image)

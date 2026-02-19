import math
from dataclasses import dataclass
from pathlib import Path
from typing import Self
from uuid import uuid4

_ICON_SIZE = 64
_MAX_ATLAS_SIZE = 4096


@dataclass(frozen=True)
class _AtlasLayout:
    """Defines the size and column structure of a square^2 texture atlas."""

    cols: int
    size: int

    @classmethod
    def new(cls, file_count: int, icon_size: int) -> Self:
        """Create an atlas layout sized to fit the given number of icons."""
        atlas_size = cls._compute_atlas_size(file_count)
        return cls(
            size=atlas_size, cols=cls._compute_cols(atlas_size, icon_size)
        )

    @staticmethod
    def _next_power_of_two(value: int) -> int:
        return 1 << (value - 1).bit_length()

    @staticmethod
    def _compute_atlas_size(file_count: int) -> int:
        icons_per_row = math.ceil(math.sqrt(file_count))
        required_pixels = icons_per_row * _ICON_SIZE

        atlas_size = _AtlasLayout._next_power_of_two(required_pixels)
        if atlas_size > _MAX_ATLAS_SIZE:
            msg = "Too many icons for a single atlas"
            raise ValueError(msg)

        return atlas_size

    @staticmethod
    def _compute_cols(atlas_size: int, icon_size: int) -> int:
        return atlas_size // icon_size


@dataclass(frozen=True)
class _AtlasCell:
    """Stores UV cell size and half-texel offset metadata for an atlas."""

    half_texel: float
    size: float
    icon_size: int

    @classmethod
    def new(cls, atlas: _AtlasLayout, icon_size: int) -> Self:
        """Create atlas cell metadata derived from the atlas layout."""
        return cls(
            size=cls._compute_cell(atlas.size, icon_size),
            half_texel=cls._compute_half_texel(atlas.size),
            icon_size=icon_size,
        )

    @staticmethod
    def _compute_cell(atlas_size: int, icon_size: int) -> float:
        return icon_size / atlas_size

    @staticmethod
    def _compute_half_texel(atlas_size: int) -> float:
        return 1 / atlas_size / 2


@dataclass(frozen=True)
class _AtlasPath:
    """Encapsulates all filesystem paths required for an atlas."""

    atlas: Path
    resource: Path
    image: Path

    @classmethod
    def new(
        cls,
        mod_path: Path,
        atlas_name: str,
        resource_uuid: str,
    ) -> Self:
        """Create directory paths for atlas, resource, and image files."""
        return cls(
            atlas=cls._get_atlas_path(mod_path, atlas_name),
            resource=cls._get_resource_path(
                mod_path, atlas_name, resource_uuid
            ),
            image=cls._get_image_path(mod_path, atlas_name),
        )

    @staticmethod
    def _get_atlas_path(mod_path: Path, atlas_name: str) -> Path:
        path = mod_path / "GUI" / f"{atlas_name}.lsx"
        path.parent.mkdir(parents=True, exist_ok=True)
        return path

    @staticmethod
    def _get_resource_path(
        mod_path: Path, atlas_name: str, resource_uuid: str
    ) -> Path:
        path = (
            mod_path
            / "Content"
            / f"[PAK]_{atlas_name}"
            / f"{resource_uuid}.lsx"
        )
        path.parent.mkdir(parents=True, exist_ok=True)
        return path

    @staticmethod
    def _get_image_path(mod_path: Path, atlas_name: str) -> Path:
        path = mod_path / "Assets" / "Textures" / "Icons" / f"{atlas_name}.png"
        path.parent.mkdir(parents=True, exist_ok=True)
        return path


@dataclass(frozen=True)
class Atlas:
    """Represents a fully configured texture atlas."""

    name: str
    mod_folder: str
    resource_uuid: str
    layout: _AtlasLayout
    path: _AtlasPath
    cell: _AtlasCell

    @classmethod
    def from_icon_count(
        cls,
        file_count: int,
        atlas_name: str,
        out_path: Path,
        mod_folder: str,
        resource_uuid: str | None,
    ) -> Self:
        """Construct a complete Atlas instance from a given icon count."""
        layout = _AtlasLayout.new(file_count, _ICON_SIZE)
        mod_path = out_path / mod_folder
        resource_uuid = resource_uuid or str(uuid4())
        return cls(
            name=atlas_name,
            resource_uuid=resource_uuid,
            mod_folder=mod_folder,
            layout=layout,
            path=_AtlasPath.new(mod_path, atlas_name, resource_uuid),
            cell=_AtlasCell.new(layout, _ICON_SIZE),
        )

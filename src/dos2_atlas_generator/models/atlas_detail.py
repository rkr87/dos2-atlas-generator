import math
from dataclasses import dataclass
from pathlib import Path
from typing import Self
from uuid import uuid4

_ICON_SIZE = 64
_MAX_ATLAS_SIZE = 4096


@dataclass(frozen=True)
class AtlasDetail:
    """Represents the layout of a texture atlas for icons."""

    name: str
    size: int
    cell: float
    half: float
    cols: int
    rows: int
    icon_size: int
    _out_dir: Path
    mod_folder: str
    resource_uuid: str

    @property
    def atlas_path(self) -> Path:
        """Return the path to the atlas LSX file."""
        path = self._out_dir / self.mod_folder / "GUI" / f"{self.name}.lsx"
        path.parent.mkdir(parents=True, exist_ok=True)
        return path

    @property
    def resource_path(self) -> Path:
        """Return the path to the resource LSX file."""
        path = (
            self._out_dir
            / self.mod_folder
            / "Content"
            / f"[PAK]_{self.name}"
            / f"{self.resource_uuid}.lsx"
        )
        path.parent.mkdir(parents=True, exist_ok=True)
        return path

    @property
    def image_path(self) -> Path:
        """Return the path to the atlas PNG image."""
        path = (
            self._out_dir
            / self.mod_folder
            / "Assets"
            / "Textures"
            / "Icons"
            / f"{self.name}.png"
        )
        path.parent.mkdir(parents=True, exist_ok=True)
        return path

    @classmethod
    def from_file_count(
        cls,
        file_count: int,
        atlas_name: str,
        out_dir: Path,
        mod_folder: str,
        resource_uuid: str | None,
    ) -> Self:
        """Create an AtlasLayout based on the number of files."""
        atlas_size = cls._compute_atlas_size(file_count)
        cols = cls._compute_cols(atlas_size)
        rows = cls._compute_rows(file_count, cols)

        return cls(
            name=atlas_name,
            size=atlas_size,
            cell=cls._compute_cell(atlas_size),
            half=cls._compute_half(atlas_size),
            cols=cols,
            rows=rows,
            icon_size=_ICON_SIZE,
            _out_dir=out_dir,
            mod_folder=mod_folder,
            resource_uuid=resource_uuid or str(uuid4()),
        )

    @staticmethod
    def _compute_atlas_size(file_count: int) -> int:
        icons_per_row = math.ceil(math.sqrt(file_count))
        required_pixels = icons_per_row * _ICON_SIZE

        atlas_size = AtlasDetail._next_power_of_two(required_pixels)

        if atlas_size > _MAX_ATLAS_SIZE:
            msg = "Too many icons for a single atlas"
            raise ValueError(msg)

        return atlas_size

    @staticmethod
    def _next_power_of_two(value: int) -> int:
        return 1 << (value - 1).bit_length()

    @staticmethod
    def _compute_cols(atlas_size: int) -> int:
        return atlas_size // _ICON_SIZE

    @staticmethod
    def _compute_rows(file_count: int, cols: int) -> int:
        return math.ceil(file_count / cols)

    @staticmethod
    def _compute_cell(atlas_size: int) -> float:
        return _ICON_SIZE / atlas_size

    @staticmethod
    def _compute_half(atlas_size: int) -> float:
        return 1 / atlas_size / 2

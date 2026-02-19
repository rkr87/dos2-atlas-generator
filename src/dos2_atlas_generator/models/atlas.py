import math
from dataclasses import dataclass
from typing import Self

_MAX_ATLAS_SIZE = 4096


@dataclass(frozen=True)
class _AtlasLayout:
    """Defines the size and column structure of a square^2 texture atlas."""

    cols: int
    size: int
    icon_size: int

    @classmethod
    def new(cls, file_count: int, icon_size: int) -> Self:
        """Create an atlas layout sized to fit the given number of icons."""
        atlas_size = cls._compute_atlas_size(file_count, icon_size)
        return cls(
            size=atlas_size,
            cols=cls._compute_cols(atlas_size, icon_size),
            icon_size=icon_size,
        )

    @staticmethod
    def _next_power_of_two(value: int) -> int:
        return 1 << (value - 1).bit_length()

    @staticmethod
    def _compute_atlas_size(file_count: int, icon_size: int) -> int:
        icons_per_row = math.ceil(math.sqrt(file_count))
        required_pixels = icons_per_row * icon_size

        atlas_size = _AtlasLayout._next_power_of_two(required_pixels)
        if atlas_size > _MAX_ATLAS_SIZE:
            msg = "Too many icons for a single atlas"
            raise ValueError(msg)

        return atlas_size

    @staticmethod
    def _compute_cols(atlas_size: int, icon_size: int) -> int:
        return atlas_size // icon_size


@dataclass(frozen=True)
class _AtlasUVCell:
    """Stores UV cell size and half-texel offset metadata for an atlas."""

    half_texel: float
    size: float

    @classmethod
    def new(cls, layout: _AtlasLayout) -> Self:
        """Create atlas cell metadata derived from the atlas layout."""
        return cls(
            size=cls._compute_cell(layout),
            half_texel=cls._compute_half_texel(layout.size),
        )

    @staticmethod
    def _compute_cell(layout: _AtlasLayout) -> float:
        return layout.icon_size / layout.size

    @staticmethod
    def _compute_half_texel(atlas_size: int) -> float:
        return 1 / atlas_size / 2


@dataclass(frozen=True)
class Atlas:
    """Represents a fully configured texture atlas."""

    layout: _AtlasLayout
    uv_cell: _AtlasUVCell

    @classmethod
    def from_icon_count(
        cls,
        file_count: int,
        icon_size: int,
    ) -> Self:
        """Construct a complete Atlas instance from a given icon count."""
        layout = _AtlasLayout.new(file_count, icon_size)
        return cls(
            layout=layout,
            uv_cell=_AtlasUVCell.new(layout),
        )

from dataclasses import dataclass
from typing import Self

from models.atlas import Atlas


@dataclass(frozen=True)
class IconNode:
    """Represents a single icon entry within a texture atlas."""

    map_key: str
    x: int
    y: int
    x_start: float
    x_end: float
    y_start: float
    y_end: float

    @classmethod
    def from_index(
        cls,
        index: int,
        map_key: str,
        atlas: Atlas,
    ) -> Self:
        """Create an IconNode from a linear atlas index."""
        x, y = cls._compute_grid_pos(index, atlas.layout.cols)

        return cls(
            map_key=map_key,
            x=x,
            y=y,
            x_start=cls._compute_start(x, atlas),
            x_end=cls._compute_end(x, atlas),
            y_start=cls._compute_start(y, atlas),
            y_end=cls._compute_end(y, atlas),
        )

    @staticmethod
    def _compute_grid_pos(index: int, cols: int) -> tuple[int, int]:
        return index % cols, index // cols

    @staticmethod
    def _compute_start(pos: int, atlas: Atlas) -> float:
        return pos * atlas.uv_cell.size + atlas.uv_cell.half_texel

    @staticmethod
    def _compute_end(pos: int, atlas: Atlas) -> float:
        return (pos + 1) * atlas.uv_cell.size - atlas.uv_cell.half_texel

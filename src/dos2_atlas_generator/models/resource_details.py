from dataclasses import dataclass
from pathlib import Path
from typing import Self
from uuid import uuid4


@dataclass(frozen=True)
class ResourceDetails:
    """Encapsulates all filesystem paths required for an atlas."""

    uvmap_path: Path
    resource_path: Path
    image_path: Path
    mod_folder: str
    resource_uuid: str
    atlas_name: str

    @classmethod
    def new(
        cls,
        output_path: Path,
        atlas_name: str,
        resource_uuid: str | None,
        mod_folder: str,
    ) -> Self:
        """Create directory paths for atlas, resource, and image files."""
        mod_path = output_path / mod_folder
        resource_uuid = resource_uuid or str(uuid4())
        return cls(
            uvmap_path=cls._get_uvmap_path(mod_path, atlas_name),
            resource_path=cls._get_resource_path(
                mod_path, atlas_name, resource_uuid
            ),
            image_path=cls._get_image_path(mod_path, atlas_name),
            mod_folder=mod_folder,
            resource_uuid=resource_uuid,
            atlas_name=atlas_name,
        )

    @staticmethod
    def _get_uvmap_path(mod_path: Path, atlas_name: str) -> Path:
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

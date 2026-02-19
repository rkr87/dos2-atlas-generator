from dataclasses import asdict
from pathlib import Path
from typing import Any

from converter import lsf
from models.atlas import Atlas
from models.icon_node import IconNode
from models.resource_details import ResourceDetails

_TEMPLATES = Path("./.templates")
_UVMAP = _TEMPLATES / "uvmap.lsx"
_ICON_NODE = _TEMPLATES / "icon_node.lsx"
_RESOURCE = _TEMPLATES / "resource.lsx"


def _load_template(path: Path) -> str:
    with path.open(encoding="utf-8") as f:
        return f.read()


def _render(template: str, template_vals: dict[str, Any]) -> str:
    for key, val in template_vals.items():
        template = template.replace(f"~~{key}~~", str(val))
    return template


def _generate_nodes(icon_nodes: list[IconNode]) -> str:
    template = _load_template(_ICON_NODE)
    return "\n".join(
        _render(template, asdict(node)) for node in reversed(icon_nodes)
    )


def _write_template(
    template_path: Path,
    template_vals: dict[str, Any],
    output_path: Path,
    *,
    create_lsf: bool = False,
) -> None:
    template = _load_template(template_path)
    rendered = _render(template, template_vals)
    with output_path.open("w", encoding="utf-8") as f:
        f.write(rendered)
    if create_lsf:
        lsf.from_lsx(output_path)


def write(
    atlas: Atlas, icon_nodes: list[IconNode], resource_details: ResourceDetails
) -> None:
    """Write LSX/LSF files for a given atlas."""
    vals = {
        "ICON_NODES": _generate_nodes(icon_nodes),
        "ICON_SIZE": atlas.layout.icon_size,
        "ATLAS_SIZE": atlas.layout.size,
        "ATLAS_NAME": resource_details.atlas_name,
        "RESOURCE_UUID": resource_details.resource_uuid,
        "MOD_FOLDER": resource_details.mod_folder,
    }
    _write_template(_UVMAP, vals, resource_details.uvmap_path)
    _write_template(
        _RESOURCE, vals, resource_details.resource_path, create_lsf=True
    )

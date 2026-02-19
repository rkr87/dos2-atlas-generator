from dataclasses import asdict
from pathlib import Path
from typing import Any

from converter import lsf
from models.atlas import Atlas
from models.icon_node import IconNode

_TEMPLATES = Path("./.templates")
_ATLAS = _TEMPLATES / "atlas.lsx"
_NODE = _TEMPLATES / "node.lsx"
_RESOURCE = _TEMPLATES / "resource.lsx"


def _load_template(path: Path) -> str:
    with path.open(encoding="utf-8") as f:
        return f.read()


def _render(template: str, template_vals: dict[str, Any]) -> str:
    for key, val in template_vals.items():
        template = template.replace(f"~~{key}~~", str(val))
    return template


def _generate_nodes(icon_nodes: list[IconNode]) -> str:
    template = _load_template(_NODE)
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


def write(atlas: Atlas, icon_nodes: list[IconNode]) -> None:
    """Write LSX/LSF files for a given atlas."""
    vals = {
        "ICON_NODES": _generate_nodes(icon_nodes),
        "ICON_SIZE": atlas.layout.icon_size,
        "ATLAS_SIZE": atlas.layout.size,
        "ATLAS_NAME": atlas.name,
        "RESOURCE_UUID": atlas.resource_uuid,
        "MOD_FOLDER": atlas.mod_folder,
    }
    _write_template(_ATLAS, vals, atlas.path.atlas)
    _write_template(_RESOURCE, vals, atlas.path.resource, create_lsf=True)

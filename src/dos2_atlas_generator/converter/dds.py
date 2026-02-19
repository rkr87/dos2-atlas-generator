import subprocess
from pathlib import Path

_TEXCONV_PATH = Path("./.bin/texconv.exe")


def from_png(path: Path) -> None:
    """Convert a PNG file to DDS using texconv.exe."""
    args = [
        _TEXCONV_PATH.as_posix(),
        "-f",
        "R8G8B8A8_UNORM",
        "-m",
        "1",
        "-y",
        "-o",
        path.parent.as_posix(),
        path.as_posix(),
    ]
    subprocess.run(args, check=True)  # noqa: S603

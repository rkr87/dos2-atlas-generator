import subprocess
from pathlib import Path

_DIVINE_PATH = Path("./.bin/divine.exe")


def from_lsx(path: Path) -> None:
    """Convert an LSX file to LSF using divine.exe."""
    resolved = path.resolve()
    command = [
        _DIVINE_PATH.as_posix(),
        "-g",
        "dos2de",
        "-s",
        resolved.as_posix(),
        "-d",
        resolved.with_suffix(".lsf").as_posix(),
        "-a",
        "convert-resource",
    ]
    subprocess.run(  # noqa: S603
        command,
        check=True,
    )

"""
Cross-platform Lambda build helper.

Called by Terraform's null_resource. Drops the handler plus pg8000 deps into
./build/ ready to be zipped by archive_file.

Requires: Python 3.9+ and pip on PATH (Terraform calls this with `python build.py`).
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BUILD = ROOT / "build"


def main() -> None:
    if BUILD.exists():
        shutil.rmtree(BUILD)
    BUILD.mkdir()

    # Copy the handler in.
    shutil.copy(ROOT / "db_bootstrap.py", BUILD / "db_bootstrap.py")
    shutil.copy(ROOT / "scheduler.py", BUILD / "scheduler.py")

    # Install pure-Python pg8000 (and its scramp dependency).
    subprocess.check_call(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "--target",
            str(BUILD),
            "--no-compile",
            "--quiet",
            "pg8000>=1.30",
        ]
    )

    # Trim caches that bloat the zip with no runtime value.
    # Keep *.dist-info: pg8000 reads scramp's metadata via importlib.metadata
    # at import time and fails with "No package metadata was found for scramp"
    # if those directories are stripped.
    for path in BUILD.rglob("__pycache__"):
        shutil.rmtree(path, ignore_errors=True)

    print(f"Built Lambda package in {BUILD}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""One-click build: sync skills -> build wheel -> remove skills from package. Run this script to complete packaging."""
import shutil
import subprocess
import sys
from pathlib import Path


def main():
    root = Path(__file__).resolve().parent
    src = root / "skills"
    dst = root / "src" / "seekdb_plugin_installer" / "skills"

    if not src.exists():
        raise SystemExit("skills/ directory not found in project root. Please create it first.")

    # 1. Sync skills -> package
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__"))
    print("Synced skills/ -> src/seekdb_plugin_installer/skills/")

    try:
        # 2. Build wheel
        print("Building wheel...")
        subprocess.run(
            [sys.executable, "-m", "build"],
            cwd=root,
            check=True,
        )
    finally:
        # 3. Remove skills from package (restore to only project root)
        if dst.exists():
            shutil.rmtree(dst)
            print("Removed src/seekdb_plugin_installer/skills/")

    print("Build complete, artifacts in dist/")


if __name__ == "__main__":
    main()

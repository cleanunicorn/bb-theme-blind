#!/usr/bin/env python3
"""Install Blind into the bb instance selected by your bb CLI."""
import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def run_bb(executable, *args):
    return subprocess.run(
        [executable, *args], check=True, capture_output=True, text=True
    ).stdout.strip()


def install(theme_root, source):
    """Atomically replace the theme, preserving an existing file in a unique backup."""
    destination = theme_root / "blind" / "theme.css"
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.is_symlink():
        raise ValueError(f"Refusing to replace a symlink: {destination}")
    backup = None
    if destination.exists():
        with tempfile.NamedTemporaryFile(
            prefix="theme-", suffix=".css.bak", dir=destination.parent, delete=False
        ) as handle:
            backup = Path(handle.name)
        shutil.copy2(destination, backup)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            prefix=".theme-", suffix=".tmp", dir=destination.parent, delete=False
        ) as handle:
            temporary = Path(handle.name)
        shutil.copy2(source, temporary)
        temporary.replace(destination)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    return destination, backup


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--no-activate", action="store_true", help="install without selecting the palette"
    )
    args = parser.parse_args(argv)
    try:
        executable = shutil.which("bb")
        if not executable:
            raise ValueError("bb is not on PATH. Install or enable the bb CLI first.")
        source = Path(__file__).resolve().with_name("theme.css")
        if not source.is_file():
            raise ValueError(f"Theme stylesheet is missing: {source}")
        directory = run_bb(executable, "theme", "dir")
        theme_root = Path(directory)
        if not directory or not theme_root.is_absolute():
            raise ValueError(f"bb theme dir did not return an absolute path: {directory!r}")
        destination, backup = install(theme_root, source)
        print(f"Installed: {destination}")
        if backup:
            print(f"Previous stylesheet backed up: {backup}")
        if args.no_activate:
            print("Select Settings > Appearance > Palette > blind, or run: bb theme set blind")
        else:
            print(run_bb(executable, "theme", "set", "blind"))
        return 0
    except subprocess.CalledProcessError as error:
        print(f"bb command failed: {error.stderr.strip() or str(error)}", file=sys.stderr)
        return 1
    except (OSError, ValueError) as error:
        print(f"Installation failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

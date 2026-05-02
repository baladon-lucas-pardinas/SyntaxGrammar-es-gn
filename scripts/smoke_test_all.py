#!/usr/bin/env python3

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    scripts = [
        REPO_ROOT / "scripts" / "smoke_test_synthetic.py",
        REPO_ROOT / "scripts" / "smoke_test_ancora.py",
    ]

    for script in scripts:
        print(f"\nRunning {script.name}...")
        subprocess.run([sys.executable, str(script)], cwd=REPO_ROOT, check=True)

    print("\nAll smoke tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

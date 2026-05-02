#!/usr/bin/env python3

from __future__ import annotations

import csv
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
WRAPPER = REPO_ROOT / "scripts" / "run_pipeline.py"


def csv_row_count(path: Path) -> int:
    with path.open("r", encoding="utf-8") as handle:
        return sum(1 for _ in csv.reader(handle))


def require(path: Path) -> None:
    if not path.exists():
        raise SystemExit(f"Missing expected file: {path}")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="syntaxgrammar-synthetic-") as temp_dir:
        output_dir = Path(temp_dir)
        run_name = "smoke-synthetic"
        run_dir = output_dir / "synthetic" / run_name

        command = [
            sys.executable,
            str(WRAPPER),
            "synthetic",
            "--run-name",
            run_name,
            "--output-dir",
            str(output_dir),
            "--subject",
            "pronoun",
            "--candidate-count",
            "500",
            "--max-translations",
            "1",
            "--seed",
            "7",
            "--overwrite",
        ]

        subprocess.run(command, cwd=REPO_ROOT, check=True)

        expected_files = [
            run_dir / "feature-grammar-config.yaml",
            run_dir / "feature-grammar.txt",
            run_dir / "cfg-grammar.txt",
            run_dir / "output.txt",
            run_dir / "trees.txt",
            run_dir / "translations.csv",
        ]
        for path in expected_files:
            require(path)

        if csv_row_count(run_dir / "translations.csv") == 0:
            raise SystemExit("Synthetic smoke test produced an empty translations.csv")

        print("Synthetic smoke test passed.")
        print(f"Artifacts: {run_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

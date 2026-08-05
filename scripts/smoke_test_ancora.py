#!/usr/bin/env python3

from __future__ import annotations

import csv
import re
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
WRAPPER = REPO_ROOT / "scripts" / "run_pipeline.py"
FIXTURE = REPO_ROOT / "tests" / "fixtures" / "ancora_smoke.txt"


def csv_rows(path: Path) -> list[list[str]]:
    with path.open("r", encoding="utf-8") as handle:
        return list(csv.reader(handle))


def require(path: Path) -> None:
    if not path.exists():
        raise SystemExit(f"Missing expected file: {path}")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="syntaxgrammar-ancora-") as temp_dir:
        output_dir = Path(temp_dir)
        run_name = "smoke-ancora"
        run_dir = output_dir / "ancora" / run_name

        command = [
            sys.executable,
            str(WRAPPER),
            "ancora",
            "--input",
            str(FIXTURE),
            "--grammar-version",
            "v9",
            "--run-name",
            run_name,
            "--output-dir",
            str(output_dir),
            "--overwrite",
        ]

        subprocess.run(command, cwd=REPO_ROOT, check=True)

        expected_files = [
            run_dir / "extracted.csv",
            run_dir / "trees.txt",
            run_dir / "indices.csv",
            run_dir / "indices_out.csv",
            run_dir / "translations.csv",
            run_dir / "output.csv",
        ]
        for path in expected_files:
            require(path)

        rows = csv_rows(run_dir / "output.csv")
        if not rows:
            raise SystemExit("Ancora smoke test produced an empty output.csv")

        polite_pattern = re.compile(r"\b(?:usted|ustedes)\b", re.IGNORECASE)
        for row in rows:
            if len(row) < 2:
                raise SystemExit(f"Unexpected row shape in output.csv: {row}")
            if polite_pattern.search(row[1]):
                raise SystemExit(
                    f"Ancora smoke test found untranslated polite pronoun in Guarani output: {row[1]}"
                )

        print("Ancora smoke test passed.")
        print(f"Artifacts: {run_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

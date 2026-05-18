#!/usr/bin/env python3

from __future__ import annotations

import csv
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
WRAPPER = REPO_ROOT / "scripts" / "run_pipeline.py"
ANCORA_FIXTURE = REPO_ROOT / "tests" / "fixtures" / "ancora_adverbs_smoke.txt"
SOLO_PATTERN = re.compile(r"\bsolo\b", re.IGNORECASE)


def csv_rows(path: Path) -> list[list[str]]:
    with path.open("r", encoding="utf-8") as handle:
        return list(csv.reader(handle))


def line_count(path: Path) -> int:
    with path.open("r", encoding="utf-8") as handle:
        return sum(1 for _ in handle)


def require(path: Path) -> None:
    if not path.exists():
        raise SystemExit(f"Missing expected file: {path}")


def contains_solo(text: str) -> bool:
    return bool(SOLO_PATTERN.search(text))


def write_synthetic_base_config(work_dir: Path) -> Path:
    adverbs_path = work_dir / "adverbs.csv"
    config_path = work_dir / "synthetic-base-config.yaml"

    adverbs_path.write_text("ae,solo,solo,R\n", encoding="utf-8")
    config = {
        "verbs": "../../guarani/verbs/matched-verbs-guarani.csv",
        "nouns": "../../guarani/nouns/finished-nouns.csv",
        "transitivities": "../../spanish/transitivity/ancora-rae/merged-transitivities.csv",
        "determiners": "../../spanish/spanish-determiners/determiners.csv",
        "pronouns": "../../spanish/spanish-pronouns/pronouns.csv",
        "adpositions": "../../guarani/adpositions/adpositions.csv",
        "adjectives": "../../guarani/adjectives/matched-adjectives-guarani.csv",
        "adverbs": str(adverbs_path),
        "output": "ignored-by-wrapper.txt",
    }
    config_path.write_text(yaml.safe_dump(config, sort_keys=False), encoding="utf-8")
    return config_path


def run_synthetic_probe(work_dir: Path) -> None:
    output_dir = work_dir / "synthetic-runs"
    run_name = "smoke-adverb-synthetic"
    run_dir = output_dir / "synthetic" / run_name
    config_path = write_synthetic_base_config(work_dir)

    command = [
        sys.executable,
        str(WRAPPER),
        "synthetic",
        "--grammar-name",
        "tenth-grammar",
        "--grammar-config",
        str(config_path),
        "--subject",
        "pronoun",
        "--candidate-count",
        "500",
        "--max-translations",
        "1",
        "--seed",
        "7",
        "--run-name",
        run_name,
        "--output-dir",
        str(output_dir),
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

    feature_grammar_text = (run_dir / "feature-grammar.txt").read_text(encoding="utf-8")
    if "R -> 'solo'" not in feature_grammar_text:
        raise SystemExit(
            "Synthetic adverb smoke test did not materialize the solo adverb rule"
        )

    rows = csv_rows(run_dir / "translations.csv")
    if not rows:
        raise SystemExit(
            "Synthetic adverb smoke test produced an empty translations.csv"
        )

    solo_rows = [row for row in rows if len(row) >= 2 and contains_solo(row[0])]
    if not solo_rows:
        raise SystemExit(
            "Synthetic adverb smoke test did not generate any source rows containing 'solo'"
        )

    leaked_rows = [row for row in solo_rows if contains_solo(row[1])]
    if leaked_rows:
        raise SystemExit(
            f"Synthetic adverb smoke test left Spanish 'solo' untranslated in Guarani output: {leaked_rows[0]}"
        )

    print("Adverb synthetic smoke test passed.")
    print(f"Artifacts: {run_dir}")


def run_ancora_probe(work_dir: Path) -> None:
    output_dir = work_dir / "ancora-runs"
    run_name = "smoke-adverb-ancora"
    run_dir = output_dir / "ancora" / run_name

    command = [
        sys.executable,
        str(WRAPPER),
        "ancora",
        "--input",
        str(ANCORA_FIXTURE),
        "--grammar-version",
        "v10",
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
        run_dir / "unparsed.txt",
    ]
    for path in expected_files:
        require(path)

    if line_count(run_dir / "unparsed.txt") != 0:
        raise SystemExit("Ancora adverb smoke test left content in unparsed.txt")

    rows = csv_rows(run_dir / "output.csv")
    if len(rows) != 3:
        raise SystemExit(
            f"Ancora adverb smoke test expected 3 output rows, got {len(rows)}"
        )

    for row in rows:
        if len(row) < 2:
            raise SystemExit(f"Unexpected row shape in output.csv: {row}")
        if not contains_solo(row[0]):
            raise SystemExit(
                f"Ancora adverb smoke fixture row lost its source adverb: {row}"
            )
        if contains_solo(row[1]):
            raise SystemExit(
                f"Ancora adverb smoke test found untranslated Spanish 'solo' in Guarani output: {row[1]}"
            )

    print("Adverb Ancora smoke test passed.")
    print(f"Artifacts: {run_dir}")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="syntaxgrammar-adverbs-") as temp_dir:
        work_dir = Path(temp_dir)
        run_synthetic_probe(work_dir)
        run_ancora_probe(work_dir)

    print("Adverb smoke test passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

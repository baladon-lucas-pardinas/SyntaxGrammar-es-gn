#!/usr/bin/env python3

from __future__ import annotations

import argparse
import csv
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover - import error path
    raise SystemExit(
        "PyYAML is required for the wrapper CLI. Install dependencies with 'python -m pip install -r requirements.txt'."
    ) from exc


REPO_ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable
DEFAULT_RUNS_DIR = REPO_ROOT / "runs"


class PipelineError(RuntimeError):
    pass


def timestamped_name(prefix: str) -> str:
    return f"{prefix}-{datetime.now().strftime('%Y%m%d-%H%M%S')}"


def resolve_repo_path(value: str | Path) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    return (REPO_ROOT / path).resolve()


def ensure_clean_run_dir(run_dir: Path, overwrite: bool) -> None:
    if run_dir.exists():
        if overwrite:
            shutil.rmtree(run_dir)
        else:
            raise PipelineError(
                f"Run directory already exists: {run_dir}. Pass --overwrite to replace it."
            )
    run_dir.mkdir(parents=True, exist_ok=True)


def run_command(command: list[str], cwd: Path, stdout_path: Path | None = None) -> None:
    printable = " ".join(command)
    print(f"\n[{cwd}] $ {printable}")
    stdout_handle = None
    try:
        if stdout_path is not None:
            stdout_path.parent.mkdir(parents=True, exist_ok=True)
            stdout_handle = stdout_path.open("w", encoding="utf-8")

        subprocess.run(
            command,
            cwd=str(cwd),
            check=True,
            stdout=stdout_handle,
        )
    except subprocess.CalledProcessError as exc:
        raise PipelineError(
            f"Command failed with exit code {exc.returncode}: {printable}"
        ) from exc
    finally:
        if stdout_handle is not None:
            stdout_handle.close()


def line_count(path: Path) -> int:
    if not path.exists():
        return 0
    with path.open("r", encoding="utf-8") as handle:
        return sum(1 for _ in handle)


def csv_row_count(path: Path) -> int:
    if not path.exists():
        return 0
    with path.open("r", encoding="utf-8") as handle:
        return sum(1 for _ in csv.reader(handle))


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    return data or {}


def write_yaml(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        yaml.safe_dump(data, handle, sort_keys=False)


def build_feature_grammar_config(base_config_path: Path, output_path: Path) -> dict:
    base_config = load_yaml(base_config_path)
    grammar_root = REPO_ROOT / "grammar" / "grammars"
    resolved = {}
    for key, value in base_config.items():
        if key == "output":
            continue
        if isinstance(value, str):
            value_path = Path(value)
            if value_path.is_absolute():
                resolved[key] = str(value_path)
            else:
                resolved[key] = str((grammar_root / value_path).resolve())
        else:
            resolved[key] = value

    resolved["output"] = str(output_path.resolve())
    return resolved


def truncate_ancora_input(
    input_path: Path, truncated_path: Path, max_sentences: int
) -> Path:
    sentences_written = 0
    with (
        input_path.open("r", encoding="utf-8") as source,
        truncated_path.open("w", encoding="utf-8") as target,
    ):
        for line in source:
            if line.startswith("# text = "):
                target.write(line)
                sentences_written += 1
                if sentences_written >= max_sentences:
                    break

    if sentences_written == 0:
        raise PipelineError(f"No '# text = ' lines were found in {input_path}")

    return truncated_path


def print_run_summary(mode: str, run_dir: Path, artifacts: dict[str, Path]) -> None:
    print(f"\nCompleted {mode} pipeline.")
    print(f"Run directory: {run_dir}")
    for label, artifact in artifacts.items():
        print(f"- {label}: {artifact}")


def run_synthetic_pipeline(args: argparse.Namespace) -> None:
    output_dir = resolve_repo_path(args.output_dir)
    run_name = args.run_name or timestamped_name("synthetic")
    run_dir = output_dir / "synthetic" / run_name
    ensure_clean_run_dir(run_dir, args.overwrite)

    grammar_dir = REPO_ROOT / "grammar" / "grammars" / args.grammar_name
    if not grammar_dir.exists():
        raise PipelineError(f"Synthetic grammar directory not found: {grammar_dir}")

    if args.grammar_config is not None:
        base_config_path = resolve_repo_path(args.grammar_config)
    else:
        base_config_path = grammar_dir / "config.yaml"

    word_weights_path = resolve_repo_path(args.word_weights)

    feature_grammar_path = run_dir / "feature-grammar.txt"
    feature_config_path = run_dir / "feature-grammar-config.yaml"
    cfg_grammar_path = run_dir / "cfg-grammar.txt"
    generated_sentences_path = run_dir / "output.txt"
    trees_path = run_dir / "trees.txt"
    translations_path = run_dir / "translations.csv"

    feature_config = build_feature_grammar_config(
        base_config_path, feature_grammar_path
    )
    write_yaml(feature_config_path, feature_config)

    run_command(
        [
            PYTHON,
            f"{args.grammar_name}/create-featgram.py",
            "-c",
            str(feature_config_path),
            "-s",
            args.subject,
        ],
        cwd=REPO_ROOT / "grammar" / "grammars",
    )

    run_command(
        [
            PYTHON,
            "cfg-grammar.py",
            str(feature_grammar_path),
            str(cfg_grammar_path),
            "-w",
            str(word_weights_path),
        ],
        cwd=REPO_ROOT / "grammar",
    )

    generation_command = [
        PYTHON,
        "weighted-generate-sentences.py",
        "-n",
        str(args.candidate_count),
        "-o",
        str(generated_sentences_path),
        str(cfg_grammar_path),
        str(feature_grammar_path),
        "-t",
        str(trees_path),
    ]
    if args.seed is not None:
        generation_command += ["--seed", str(args.seed)]

    run_command(generation_command, cwd=REPO_ROOT / "grammar")

    if line_count(trees_path) == 0:
        raise PipelineError(
            "Synthetic generation produced no parseable trees. Increase --candidate-count or choose a different --subject."
        )

    run_command(
        [
            PYTHON,
            "-m",
            "translate.translate_trees",
            str(trees_path),
            "rules.json",
            "-o",
            str(translations_path),
            "--max-translations",
            str(args.max_translations),
        ],
        cwd=REPO_ROOT / "grammar" / "guarani",
    )

    if csv_row_count(translations_path) == 0:
        raise PipelineError("Synthetic translation produced an empty CSV output.")

    print_run_summary(
        "synthetic",
        run_dir,
        {
            "feature grammar config": feature_config_path,
            "feature grammar": feature_grammar_path,
            "cfg grammar": cfg_grammar_path,
            "generated sentences": generated_sentences_path,
            "trees": trees_path,
            "translations": translations_path,
        },
    )


def run_ancora_pipeline(args: argparse.Namespace) -> None:
    output_dir = resolve_repo_path(args.output_dir)
    run_name = args.run_name or timestamped_name("ancora")
    run_dir = output_dir / "ancora" / run_name
    ensure_clean_run_dir(run_dir, args.overwrite)

    input_path = resolve_repo_path(args.input)
    grammar_dir = REPO_ROOT / "grammar" / "ancora" / args.grammar_version
    feature_grammar_path = grammar_dir / "feature-grammar.txt"
    if not feature_grammar_path.exists():
        raise PipelineError(f"Feature grammar not found: {feature_grammar_path}")

    effective_input = input_path
    if args.max_sentences is not None:
        effective_input = truncate_ancora_input(
            input_path,
            run_dir / "ancora-truncated.txt",
            args.max_sentences,
        )

    extracted_path = run_dir / "extracted.csv"
    trees_path = run_dir / "trees.txt"
    indices_path = run_dir / "indices.csv"
    indices_out_path = run_dir / "indices_out.csv"
    unparsed_path = run_dir / "unparsed.txt"
    translations_path = run_dir / "translations.csv"
    untranslated_path = run_dir / "untranslated.csv"
    output_path = run_dir / "output.csv"

    run_command(
        [
            PYTHON,
            "../parsing-subtrees/extract-ancora-sentences.py",
            str(effective_input),
            str(extracted_path),
        ],
        cwd=REPO_ROOT / "grammar" / "ancora",
    )

    run_command(
        [
            PYTHON,
            "../../parsing-subtrees/parse-subtrees-3.py",
            "--grammar",
            str(feature_grammar_path),
            "--input",
            str(extracted_path),
            "--output",
            str(trees_path),
            "--indices",
            str(indices_path),
            "--nonparsed",
            str(unparsed_path),
        ],
        cwd=grammar_dir,
    )

    if line_count(trees_path) == 0:
        raise PipelineError("Ancora parsing produced no trees.")

    run_command(
        [
            PYTHON,
            "-m",
            "translate.translate_ancora",
            str(trees_path),
            "rules-ancora.json",
            "-o",
            str(translations_path),
            "--indices",
            str(indices_path),
        ],
        cwd=REPO_ROOT / "grammar" / "guarani",
        stdout_path=untranslated_path,
    )

    if not indices_out_path.exists():
        generated_indices_out = indices_path.with_name(indices_path.stem + "_out.csv")
        if generated_indices_out.exists():
            generated_indices_out.replace(indices_out_path)
        else:
            raise PipelineError("Ancora translation did not generate indices_out.csv")

    run_command(
        [
            PYTHON,
            "embed-guarani.py",
            "--indices",
            str(indices_out_path),
            "--extracted",
            str(extracted_path),
            "--translations",
            str(translations_path),
            "--output",
            str(output_path),
        ],
        cwd=REPO_ROOT / "grammar" / "ancora",
    )

    if csv_row_count(output_path) == 0:
        raise PipelineError("Ancora embedding produced an empty CSV output.")

    print_run_summary(
        "ancora",
        run_dir,
        {
            "effective input": effective_input,
            "extracted": extracted_path,
            "trees": trees_path,
            "indices": indices_path,
            "indices out": indices_out_path,
            "translations": translations_path,
            "untranslated": untranslated_path,
            "embedded output": output_path,
            "unparsed": unparsed_path,
        },
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run the Spanish->Guarani pipelines from the repository root without manual directory hopping."
    )
    subparsers = parser.add_subparsers(dest="mode", required=True)

    synthetic = subparsers.add_parser(
        "synthetic",
        help="Run the synthetic corpus pipeline",
    )
    synthetic.add_argument(
        "--grammar-name",
        default="ninth-grammar",
        help="Grammar generator directory under grammar/grammars",
    )
    synthetic.add_argument(
        "--subject",
        choices=["pronoun", "np", "adj", "all"],
        default="all",
        help="Subject profile used for feature grammar generation",
    )
    synthetic.add_argument(
        "--candidate-count",
        type=int,
        default=500,
        help="Number of CFG candidate sentences to sample before feature-grammar validation",
    )
    synthetic.add_argument(
        "--max-translations",
        type=int,
        default=1,
        help="Maximum translations to emit per Spanish tree",
    )
    synthetic.add_argument(
        "--grammar-config",
        default=None,
        help="Base feature grammar config file; defaults to <grammar-name>/config.yaml",
    )
    synthetic.add_argument(
        "--word-weights",
        default="spanish/jojajovai/word_occurrences.csv",
        help="Word frequency CSV used when building the CFG",
    )
    synthetic.add_argument(
        "--seed", type=int, default=None, help="Optional random seed"
    )
    synthetic.add_argument(
        "--run-name", default=None, help="Run name under the output directory"
    )
    synthetic.add_argument(
        "--output-dir",
        default=str(DEFAULT_RUNS_DIR),
        help="Base directory for wrapper-managed outputs",
    )
    synthetic.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace an existing run directory with the same name",
    )

    ancora = subparsers.add_parser(
        "ancora",
        help="Run the Ancora corpus pipeline",
    )
    ancora.add_argument(
        "--input",
        default="ancora/ancora-sentences/ancora_all.txt",
        help="Ancora source file containing '# text = ...' lines",
    )
    ancora.add_argument(
        "--grammar-version",
        default="v9",
        help="Ancora grammar directory under grammar/ancora",
    )
    ancora.add_argument(
        "--max-sentences",
        type=int,
        default=None,
        help="Optional limit for extracting a small number of sentences",
    )
    ancora.add_argument(
        "--run-name", default=None, help="Run name under the output directory"
    )
    ancora.add_argument(
        "--output-dir",
        default=str(DEFAULT_RUNS_DIR),
        help="Base directory for wrapper-managed outputs",
    )
    ancora.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace an existing run directory with the same name",
    )

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.mode == "synthetic":
            run_synthetic_pipeline(args)
        elif args.mode == "ancora":
            run_ancora_pipeline(args)
        else:  # pragma: no cover - argparse prevents this path
            parser.error(f"Unknown mode: {args.mode}")
    except PipelineError as exc:
        print(f"\nPipeline failed: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

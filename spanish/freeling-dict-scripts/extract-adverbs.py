import argparse
import csv
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DICTIONARY = REPO_ROOT / "bilingual-dictionaries" / "dicc_dc.txt"
DEFAULT_OUTPUT = REPO_ROOT / "guarani" / "adverbs" / "adverbs.csv"

EXCLUDED_SPANISH = {
    "muy",
    "mucho",
    "demasiado",
    "bastante",
    "tan",
    "tanto",
    "muchísimo",
    "sumamente",
    "excesivamente",
    "extraordinariamente",
    "ultra",
    "intensamente",
    "no",
}

EXCLUDED_GUARANI = {
    "porã",
    "terei",
    "iterei",
    "eterei",
    "tove",
}


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract curated adverb pairs from dicc_dc.txt into guarani/adverbs/adverbs.csv"
    )
    parser.add_argument(
        "--dictionary",
        default=str(DEFAULT_DICTIONARY),
        help="Path to dicc_dc.txt",
    )
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT),
        help="Path to the generated adverbs CSV",
    )
    return parser.parse_args()


def normalize(value: str) -> str:
    return value.strip().casefold()


def parse_dictionary_line(line: str) -> tuple[str, str, str] | None:
    parts = line.strip().split(maxsplit=2)
    if len(parts) != 3:
        return None

    category, guarani_part, spanish_part = parts
    if not guarani_part.startswith("gn:") or not spanish_part.startswith("es:"):
        return None

    return category, guarani_part[3:], spanish_part[3:]


def should_skip(guarani: str, spanish: str) -> bool:
    normalized_guarani = normalize(guarani)
    normalized_spanish = normalize(spanish)

    if "_" in guarani or "_" in spanish:
        return True
    if normalized_spanish in EXCLUDED_SPANISH:
        return True
    if normalized_guarani in EXCLUDED_GUARANI:
        return True
    return False


def extract_adverbs(dictionary_path: Path) -> list[list[str]]:
    rows: list[list[str]] = []
    seen: set[tuple[str, str]] = set()

    with dictionary_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            parsed = parse_dictionary_line(line)
            if parsed is None:
                continue

            category, guarani, spanish = parsed
            if category != "r":
                continue
            if should_skip(guarani, spanish):
                continue

            key = (normalize(guarani), normalize(spanish))
            if key in seen:
                continue
            seen.add(key)

            rows.append([guarani, spanish, spanish, "R"])

    return rows


def write_rows(output_path: Path, rows: list[list[str]]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerows(rows)


def main() -> None:
    args = parse_arguments()
    dictionary_path = Path(args.dictionary).resolve()
    output_path = Path(args.output).resolve()

    rows = extract_adverbs(dictionary_path)
    write_rows(output_path, rows)
    print(f"Extracted {len(rows)} curated adverb pairs to {output_path}")


if __name__ == "__main__":
    main()

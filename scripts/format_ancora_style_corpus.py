#!/usr/bin/env python3

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path

DEFAULT_SEGMENT_MARKER = "<NS>"
METADATA_PREFIX_RE = re.compile(r"^\S+\s+https?://\S+\s+")
URL_RE = re.compile(r"https?://\S+")
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+(?=(?:[\"'“”‘’¿¡(\[]*[A-ZÁÉÍÓÚÜÑ0-9]))")


def strip_metadata_prefix(line: str) -> str:
    return METADATA_PREFIX_RE.sub("", line, count=1)


def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def sentence_candidates(segment: str) -> list[str]:
    segment = html.unescape(segment)
    segment = normalize_whitespace(segment)
    if not segment:
        return []
    return [normalize_whitespace(piece) for piece in SENTENCE_SPLIT_RE.split(segment)]


def is_usable_sentence(sentence: str, min_words: int) -> bool:
    if not sentence or URL_RE.search(sentence):
        return False

    words = sentence.split()
    if len(words) < min_words:
        return False

    if not any(char.isalpha() for char in sentence):
        return False

    return True


def iter_formatted_sentences(
    input_path: Path,
    segment_marker: str,
    min_words: int,
    max_records: int | None,
    max_sentences: int | None,
):
    emitted = 0

    with input_path.open("r", encoding="utf-8") as handle:
        for record_index, raw_line in enumerate(handle):
            if max_records is not None and record_index >= max_records:
                break

            line = strip_metadata_prefix(raw_line.strip())
            if not line:
                continue

            for segment in line.split(segment_marker):
                for sentence in sentence_candidates(segment):
                    if not is_usable_sentence(sentence, min_words=min_words):
                        continue

                    yield sentence
                    emitted += 1
                    if max_sentences is not None and emitted >= max_sentences:
                        return


def format_corpus(
    input_path: Path,
    output_path: Path,
    segment_marker: str,
    min_words: int,
    max_records: int | None,
    max_sentences: int | None,
) -> int:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    written = 0

    with output_path.open("w", encoding="utf-8") as output_handle:
        for sentence in iter_formatted_sentences(
            input_path=input_path,
            segment_marker=segment_marker,
            min_words=min_words,
            max_records=max_records,
            max_sentences=max_sentences,
        ):
            output_handle.write(f"# text = {sentence}\n")
            written += 1

    return written


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Convert a raw text corpus into the Ancora-style '# text = ...' format consumed by the corpus pipeline."
    )
    parser.add_argument("input", help="Path to the raw source corpus")
    parser.add_argument("output", help="Path to the formatted output file")
    parser.add_argument(
        "--segment-marker",
        default=DEFAULT_SEGMENT_MARKER,
        help="Marker used to split logical text segments inside each record",
    )
    parser.add_argument(
        "--min-words",
        type=int,
        default=4,
        help="Minimum token count required for an emitted sentence",
    )
    parser.add_argument(
        "--max-records",
        type=int,
        default=None,
        help="Optional limit on input records for quick smoke runs",
    )
    parser.add_argument(
        "--max-sentences",
        type=int,
        default=None,
        help="Optional limit on emitted sentences for quick smoke runs",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)

    written = format_corpus(
        input_path=input_path,
        output_path=output_path,
        segment_marker=args.segment_marker,
        min_words=args.min_words,
        max_records=args.max_records,
        max_sentences=args.max_sentences,
    )

    print(f"Wrote {written} Ancora-style lines to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

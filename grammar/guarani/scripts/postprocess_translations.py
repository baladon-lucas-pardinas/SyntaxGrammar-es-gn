#!/usr/bin/env python3
"""
Script to diagnose and postprocess Spanish-Guarani translation CSV files.

Commands:
    fix-t       - Diagnose and fix words ending in 'T' (invalid in Guarani)
    find-usted  - Find sentences with 'Usted' in Guarani translations

Examples:
    # Run diagnostics on words ending in 't'
    python postprocess_translations.py fix-t translations/total.csv

    # Fix words ending in 't' by appending 'a' (overwrites file)
    python postprocess_translations.py fix-t translations/total.csv --fix

    # Fix only words not present in Spanish
    python postprocess_translations.py fix-t translations/total.csv --fix --exclude-spanish-words

    # Find all sentences with 'Usted' in Guarani
    python postprocess_translations.py find-usted translations/total.csv
"""

import argparse
import csv
import re
from collections import Counter
from pathlib import Path


def read_translation_csv(csv_path):
    """Read the translation CSV file and return rows."""
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        return list(reader)


def extract_words(text):
    """Extract words from text, using spaces and punctuation (dots, commas) as separators."""
    # Split on !%),.:;?]}¿¡([{~" and spaces
    # I omitted single quotes because only 'Pinochet' is in the Ancora corpus, and we use the '
    # as the apostrophe in Guarani. What I mean the only case we'd miss is 'Pinochet' which is good
    words = re.split(r"[!\%\),\.:;\?\]\}¿¡\(\[\{\~\"\s]+", text)
    # Remove empty strings
    words = [word for word in words if word]
    return words


def split_with_separators(text):
    """
    Split text into words and separators, preserving the original structure.

    Returns:
        List of tuples (token, is_word) where is_word is True for words, False for separators
    """
    # Use the same pattern as extract_words, with a capturing group
    pattern = r"([!\%\),\.:;\?\]\}¿¡\(\[\{\~\"\s]+)"
    parts = re.split(pattern, text)

    # When using split with a capturing group, the pattern matches are included in the result
    # and alternate with non-matches. But we need to check explicitly rather than assume
    separator_pattern = r"^[!\%\),\.:;\?\]\}¿¡\(\[\{\~\"\s]+$"

    result = []
    for part in parts:
        if part:  # Skip empty strings
            is_separator = bool(re.match(separator_pattern, part))
            result.append((part, not is_separator))

    return result


def find_words_ending_in_t(text):
    """Find all words ending in 'T' in text."""
    words = extract_words(text)
    words_ending_in_t = [word for word in words if word.lower().endswith("t")]
    return words_ending_in_t


def filter_guarani_only_words(spanish_words, guarani_words):
    """
    Filter to keep only words that appear in Guarani but not in Spanish.

    Args:
        spanish_words: List of words from Spanish text
        guarani_words: List of words from Guarani text

    Returns:
        List of words that are only in Guarani
    """
    spanish_words_lower = set(word.lower() for word in spanish_words)
    return [word for word in guarani_words if word.lower() not in spanish_words_lower]


def fix_words_ending_in_t(text, spanish_text=None, exclude_spanish_words=False):
    """
    Replace words ending in 'T' with the same word ending in 'ta'.

    Args:
        text: Guarani text to process
        spanish_text: Optional Spanish text for filtering
        exclude_spanish_words: If True, only fix words not present in Spanish text

    Returns:
        Text with words ending in 't' replaced with 'ta'
    """
    words = extract_words(text)
    words_ending_in_t = [word for word in words if word.lower().endswith("t")]

    if exclude_spanish_words and spanish_text:
        spanish_words_ending_in_t = find_words_ending_in_t(spanish_text)
        words_ending_in_t = filter_guarani_only_words(
            spanish_words_ending_in_t, words_ending_in_t
        )

    # Create a set of words (lowercase) that should be replaced
    words_to_replace = set(word.lower() for word in words_ending_in_t)

    # Split text into words and separators, preserving structure
    tokens = split_with_separators(text)

    # Rebuild text, replacing words ending in 't' with 'ta'
    result_parts = []
    for token, is_word in tokens:
        if is_word and token.lower() in words_to_replace:
            # Append 'a' to the word
            result_parts.append(token + "a")
        else:
            result_parts.append(token)

    return "".join(result_parts)


def count_usted_in_guarani(guarani_text):
    """Count occurrences of 'Usted' (case-insensitive) in Guarani text."""
    # Match 'Usted' as a whole word
    matches = re.findall(r"\busted\b", guarani_text, re.IGNORECASE)
    return len(matches)


def has_usted_in_guarani(guarani_text):
    """Check if Guarani text contains 'Usted' (case-insensitive)."""
    # Use extract_words to get words, then check for 'usted'
    words = extract_words(guarani_text)
    return any(word.lower() == "usted" for word in words)


def run_diagnostics(csv_path, output_dir=None, exclude_spanish_words=False):
    """
    Run diagnostics on the translation CSV.

    Args:
        csv_path: Path to the input CSV file
        output_dir: Optional directory for output files (defaults to same as input)
        exclude_spanish_words: If True, only count words not present in Spanish text
    """
    csv_path = Path(csv_path)
    if output_dir is None:
        output_dir = csv_path.parent
    else:
        output_dir = Path(output_dir)

    print(f"Reading translations from: {csv_path}")
    rows = read_translation_csv(csv_path)

    # Collect statistics
    all_words_ending_in_t = []
    total_usted_count = 0

    for row in rows:
        if len(row) < 2:
            continue

        spanish_text = row[0]
        guarani_text = row[1]

        # Find words ending in T
        words_with_t = find_words_ending_in_t(guarani_text)

        if exclude_spanish_words:
            spanish_words_with_t = find_words_ending_in_t(spanish_text)
            words_with_t = filter_guarani_only_words(spanish_words_with_t, words_with_t)

        all_words_ending_in_t.extend(words_with_t)

        # Count Usted
        usted_count = count_usted_in_guarani(guarani_text)
        total_usted_count += usted_count

    # Get unique words ending in T
    unique_words_ending_in_t = sorted(
        set(word.lower() for word in all_words_ending_in_t)
    )

    # Report statistics
    print("\n" + "=" * 60)
    print("DIAGNOSTIC RESULTS")
    print("=" * 60)

    print(f"\nTotal sentences analyzed: {len(rows)}")

    print("\n--- Words ending in 'T' ---")
    if exclude_spanish_words:
        print("(excluding words also present in Spanish)")
    print(f"Total occurrences: {len(all_words_ending_in_t)}")
    print(f"Unique words: {len(unique_words_ending_in_t)}")

    print("\n--- 'Usted' in Guarani translations ---")
    print(f"Total occurrences: {total_usted_count}")

    # Save unique words ending in T to CSV
    output_csv = output_dir / f"{csv_path.stem}_words_ending_in_t.csv"
    with open(output_csv, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Word", "Count"])

        # Count frequency of each unique word
        word_counts = Counter(word.lower() for word in all_words_ending_in_t)
        for word in unique_words_ending_in_t:
            writer.writerow([word, word_counts[word]])

    print(f"\nUnique words ending in 'T' saved to: {output_csv}")

    # Show a sample of the most common words ending in T
    if unique_words_ending_in_t:
        print("\nMost common words ending in 'T':")
        word_counts = Counter(word.lower() for word in all_words_ending_in_t)
        for word, count in word_counts.most_common(10):
            print(f"  {word}: {count}")

    print("\n" + "=" * 60)

    return {
        "total_sentences": len(rows),
        "words_ending_in_t_total": len(all_words_ending_in_t),
        "words_ending_in_t_unique": len(unique_words_ending_in_t),
        "usted_count": total_usted_count,
        "output_csv": output_csv,
    }


def fix_csv(csv_path, exclude_spanish_words=False):
    """
    Fix the CSV by replacing words ending in 'T' with 'ta'.
    Overwrites the original file.

    Args:
        csv_path: Path to the CSV file to fix
        exclude_spanish_words: If True, only fix words not present in Spanish text
    """
    csv_path = Path(csv_path)

    print(f"Reading translations from: {csv_path}")
    rows = read_translation_csv(csv_path)

    print("Fixing words ending in 'T'...")
    if exclude_spanish_words:
        print("(excluding words also present in Spanish)")

    fixed_rows = []
    total_fixes = 0

    for row in rows:
        if len(row) < 2:
            fixed_rows.append(row)
            continue

        spanish_text = row[0]
        guarani_text = row[1]

        # Fix Guarani text
        fixed_guarani = fix_words_ending_in_t(
            guarani_text,
            spanish_text if exclude_spanish_words else None,
            exclude_spanish_words,
        )

        if fixed_guarani != guarani_text:
            total_fixes += 1

        fixed_rows.append([spanish_text, fixed_guarani])

    # Write back to the same file
    print(f"\nWriting fixed translations to: {csv_path}")
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(fixed_rows)

    print(f"Fixed {total_fixes} sentences")
    print("Done!")


def find_usted_sentences(csv_path, output_path=None, remove_from_original=False):
    """
    Find all sentences with 'Usted' in the Guarani translation.

    Args:
        csv_path: Path to the input CSV file
        output_path: Optional path for output CSV (defaults to <input>_usted.csv)
        remove_from_original: If True, remove sentences with Usted from the original file
    """
    csv_path = Path(csv_path)

    if output_path is None:
        output_path = csv_path.parent / f"{csv_path.stem}_usted.csv"
    else:
        output_path = Path(output_path)

    print(f"Reading translations from: {csv_path}")
    rows = read_translation_csv(csv_path)

    print("Searching for 'Usted' in Guarani translations...")

    usted_sentences = []
    clean_rows = []

    for idx, row in enumerate(rows):
        if len(row) < 2:
            clean_rows.append(row)
            continue

        guarani_text = row[1]

        if has_usted_in_guarani(guarani_text):
            usted_sentences.append(
                {"index": idx, "spanish": row[0], "guarani": guarani_text}
            )
        else:
            clean_rows.append(row)

    # Write results to CSV
    print(f"\nWriting results to: {output_path}")
    with open(output_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Index", "Guarani_Sentence"])

        for item in usted_sentences:
            writer.writerow([item["index"], item["guarani"]])

    print(f"\nFound {len(usted_sentences)} sentences with 'Usted' in Guarani")
    print(f"Results saved to: {output_path}")

    # Remove sentences with Usted from original file if requested
    if remove_from_original:
        print("\nRemoving sentences with 'Usted' from original file...")
        print(f"Original sentence count: {len(rows)}")
        print(f"Clean sentence count: {len(clean_rows)}")
        print(f"Removed: {len(usted_sentences)} sentences")

        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(clean_rows)

        print(f"Updated file saved to: {csv_path}")

    print("Done!")

    return usted_sentences


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Diagnose and postprocess Spanish-Guarani translation CSV files.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # ========== fix-t command ==========
    fix_t_parser = subparsers.add_parser(
        "fix-t",
        help='Diagnose and fix words ending in "t"',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run diagnostics only
  python postprocess_translations.py fix-t translations/total.csv
  
  # Run diagnostics, excluding words present in Spanish
  python postprocess_translations.py fix-t translations/total.csv --exclude-spanish-words
  
  # Fix words ending in 't' by appending 'a' (overwrites file)
  python postprocess_translations.py fix-t translations/total.csv --fix
  
  # Fix words, but only those not present in Spanish
  python postprocess_translations.py fix-t translations/total.csv --fix --exclude-spanish-words
  
  # Run diagnostics with custom output directory
  python postprocess_translations.py fix-t translations/total.csv --output-dir output/
        """,
    )

    fix_t_parser.add_argument("csv_file", help="Path to the CSV file to process")

    fix_t_parser.add_argument(
        "--output-dir",
        help="Directory for diagnostic output files (default: same as input file)",
    )

    fix_t_parser.add_argument(
        "--exclude-spanish-words",
        action="store_true",
        help="Only process words that are not present in the Spanish text of the same sentence",
    )

    fix_t_parser.add_argument(
        "--fix",
        action="store_true",
        help='Fix words ending in "t" by appending "a" to make them end in "ta" (overwrites original file)',
    )

    # ========== find-usted command ==========
    find_usted_parser = subparsers.add_parser(
        "find-usted",
        help='Find sentences with "Usted" in Guarani translations',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Find all sentences with 'Usted' in Guarani
  python postprocess_translations.py find-usted translations/total.csv
  
  # Specify custom output path
  python postprocess_translations.py find-usted translations/total.csv --output results/usted.csv
  
  # Remove sentences with 'Usted' from the original file
  python postprocess_translations.py find-usted translations/total.csv --remove
        """,
    )

    find_usted_parser.add_argument("csv_file", help="Path to the CSV file to process")

    find_usted_parser.add_argument(
        "--output", help="Path for output CSV file (default: <input>_usted.csv)"
    )

    find_usted_parser.add_argument(
        "--remove",
        action="store_true",
        help="Remove sentences with 'Usted' from the original file (overwrites original file)",
    )

    # Parse arguments
    args = parser.parse_args()

    # Show help if no command specified
    if args.command is None:
        parser.print_help()
        return

    # Execute the appropriate command
    if args.command == "fix-t":
        if args.fix:
            fix_csv(args.csv_file, args.exclude_spanish_words)
        else:
            run_diagnostics(args.csv_file, args.output_dir, args.exclude_spanish_words)

    elif args.command == "find-usted":
        find_usted_sentences(args.csv_file, args.output, args.remove)


if __name__ == "__main__":
    main()

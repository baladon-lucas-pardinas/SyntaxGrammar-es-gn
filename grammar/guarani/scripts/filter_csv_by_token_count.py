### Usage: python filter_csv_by_token_count.py <input_file> <output_file> <min_tokens> <max_tokens>

import csv
import argparse

def count_tokens(sentence):
    tokens = sentence.split()
    return len(tokens)

def filter_lines(input_file, output_file, min_tokens, max_tokens):
    with open(input_file, 'r', encoding='utf-8') as in_file, open(output_file, 'w', encoding='utf-8') as out_file:
        reader = csv.reader(in_file)
        writer = csv.writer(out_file)
        for row in reader:
            if len(row) > 0:
                spanish_sentence = row[0]
                num_tokens = count_tokens(spanish_sentence)
                if min_tokens <= num_tokens <= max_tokens:
                    writer.writerow(row)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Filter lines based on token count.")
    parser.add_argument("input_file", help="Path to the input CSV file.")
    parser.add_argument("output_file", help="Path to the output CSV file.")
    parser.add_argument("min_tokens", type=int, help="Minimum number of tokens.")
    parser.add_argument("max_tokens", type=int, help="Maximum number of tokens.")
    args = parser.parse_args()

    input_file_path = args.input_file
    output_file_path = args.output_file
    min_tokens = args.min_tokens
    max_tokens = args.max_tokens

    filter_lines(input_file_path, output_file_path, min_tokens, max_tokens)

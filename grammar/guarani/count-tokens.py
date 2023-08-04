import csv
import argparse

def count_tokens(csv_file):
    total_tokens = 0

    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) > 0:
                sentence = row[0]
                tokens = sentence.split()
                total_tokens += len(tokens)

    return total_tokens

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Count the total number of tokens in a CSV file where each cell is a sentence.")
    parser.add_argument("csv_file", help="Path to the CSV file.")
    args = parser.parse_args()

    csv_file_path = args.csv_file
    total_tokens = count_tokens(csv_file_path)
    print(f"Total number of tokens: {total_tokens}")

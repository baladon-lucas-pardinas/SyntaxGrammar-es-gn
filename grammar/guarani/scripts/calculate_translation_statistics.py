### Usage: python count-tokens.py <input_file>

import csv
import argparse
import string

def count_tokens(csv_file):
    total_tokens_spanish = 0
    total_tokens_guarani = 0
    total_sentences = 0

    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) > 0:
                sentence_spanish = row[0]
                sentence_guarani = row[1]
                tokens_spanish = sentence_spanish.split()
                tokens_guarani = sentence_guarani.split()
                total_tokens_spanish += len(tokens_spanish)
                total_tokens_guarani += len(tokens_guarani)
                total_sentences += 1

    return total_tokens_spanish, total_tokens_guarani, total_sentences

def calculate_correlation(csv_file):
    spanish_lengths = []
    guarani_lengths = []

    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) > 0:
                sentence_spanish = row[0]
                sentence_guarani = row[1]
                tokens_spanish = len(sentence_spanish.split())
                tokens_guarani = len(sentence_guarani.split())
                spanish_lengths.append(tokens_spanish)
                guarani_lengths.append(tokens_guarani)

    correlation = round(numpy.corrcoef(spanish_lengths, guarani_lengths)[0, 1], 4)
    return correlation

def calculate_vocabulary_size(csv_file):
    vocabulary_spanish = set()
    vocabulary_guarani = set()

    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) > 0:
                sentence_spanish = row[0]
                sentence_guarani = row[1]
                words_spanish = sentence_spanish.lower().translate(str.maketrans('', '', string.punctuation + "¿¡")).split()
                words_guarani = sentence_guarani.lower().translate(str.maketrans('', '', string.punctuation + "¿¡")).split()
                vocabulary_spanish.update(words_spanish)
                vocabulary_guarani.update(words_guarani)

    return len(vocabulary_spanish), len(vocabulary_guarani)

if __name__ == "__main__":
    import numpy

    parser = argparse.ArgumentParser(description="Analyze a CSV file containing sentence pairs.")
    parser.add_argument("csv_file", help="Path to the CSV file.")
    args = parser.parse_args()

    csv_file_path = args.csv_file

    total_tokens_spanish, total_tokens_guarani, total_sentences = count_tokens(csv_file_path)
    print(f"Total number of sentence pairs: {total_sentences}")
    print(f"Total number of tokens in Spanish: {total_tokens_spanish}")
    print(f"Total number of tokens in Guarani: {total_tokens_guarani}")
    
    average_tokens_spanish = total_tokens_spanish / total_sentences
    average_tokens_guarani = total_tokens_guarani / total_sentences
    print(f"Average number of tokens per sentence in Spanish: {average_tokens_spanish:.2f}")
    print(f"Average number of tokens per sentence in Guarani: {average_tokens_guarani:.2f}")

    correlation = calculate_correlation(csv_file_path)
    print(f"Sentence pair length correlation: {correlation:.4f}")

    vocabulary_size_spanish, vocabulary_size_guarani = calculate_vocabulary_size(csv_file_path)
    print(f"Vocabulary size in Spanish: {vocabulary_size_spanish}")
    print(f"Vocabulary size in Guarani: {vocabulary_size_guarani}")

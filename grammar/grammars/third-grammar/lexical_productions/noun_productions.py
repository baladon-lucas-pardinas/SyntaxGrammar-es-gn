### Read: https://www.nltk.org/book/ch09.html
import csv


def write_noun_productions(grammar_file, noun_lexicon):
    # Load noun lexical rules from CSV
    with open(noun_lexicon, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            word = row[1]
            gender = row[5]
            number = row[6]
            grammar_file.write(f"\nN[AGR=[GEN={gender.lower()}, NUM={number.lower()}, PER={'3'}]] -> '{word}'")

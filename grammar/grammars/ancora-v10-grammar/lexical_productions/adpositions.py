### Read: https://www.nltk.org/book/ch09.html
import csv


def write_adposition_productions(grammar_file, adposition_lexicon):
    # Load determiner lexical rules from CSV
    with open(adposition_lexicon, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            word = row[6]

            grammar_file.write(f"PR -> '{word}'\n")

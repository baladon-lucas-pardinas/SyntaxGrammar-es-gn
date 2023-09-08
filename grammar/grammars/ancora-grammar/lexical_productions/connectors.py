### Read: https://www.nltk.org/book/ch09.html
import csv

def write_connectors_productions(grammar_file, connectors_lexicon):
    # Load connectors lexical rules from CSV
    with open(connectors_lexicon, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            word = row[1]

            grammar_file.write(f"CON -> '{word}'\n")
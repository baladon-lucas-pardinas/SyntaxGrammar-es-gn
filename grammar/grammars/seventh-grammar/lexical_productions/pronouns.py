### Read: https://www.nltk.org/book/ch09.html
import csv


def write_pronoun_productions(grammar_file, pronoun_lexicon):
    # Load pronoun lexical rules from CSV
    with open(pronoun_lexicon, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            word = row[0]
            type = row[3].lower()
            person = row[4].lower()
            gender = row[5].lower()
            number = row[6].lower()
            case = row[7].lower()
            polite = row[8].lower()

            # Beware of this
            if (polite == 'p'): 
                person = '3'

            grammar_file.write(f"P[AGR=[ GEN={gender}, NUM={number}, PER={person}], TYPE={type}, CASE={case}, POLITE={polite}] -> '{word}'\n")

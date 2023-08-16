### Read: https://www.nltk.org/book/ch09.html
import csv


def write_adjective_productions(grammar_file, noun_lexicon):
    # Load noun lexical rules from CSV
    with open(noun_lexicon, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            shifted_row = [row[1]] + row[-9:]
            word = shifted_row[1]
            gender = shifted_row[6]
            number = shifted_row[7]
            if (gender == 'C'):
                grammar_file.write(f"A[AGR=[NUM={number.lower()}]] -> '{word}'\n")
            else:
                grammar_file.write(f"A[AGR=[GEN={gender.lower()}, NUM={number.lower()}]] -> '{word}'\n")

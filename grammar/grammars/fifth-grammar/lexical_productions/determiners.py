### Read: https://www.nltk.org/book/ch09.html
import csv


def write_determiner_productions(grammar_file, determiner_lexicon):
    # Load determiner lexical rules from CSV
    with open(determiner_lexicon, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            word = row[0]
            type = row[3].lower()
            possessor_person = row[4].lower()
            gender = row[5].lower()
            number = row[6].lower()
            possessor_num = row[7].lower()

            grammar_file.write(f"D[AGR=[ GEN={gender}, NUM={number}], TYPE={type}, POSSPER={possessor_person}, POSSNUM={possessor_num}] -> '{word}'\n")

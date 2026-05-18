### Read: https://www.nltk.org/book/ch09.html
import csv


def write_verb_productions(grammar_file, verb_lexicon, transitivities):
 # Load verb lexical rules from CSV
    with open(verb_lexicon, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            # This is to use the appropriate columns in all.verbs.csv
            shifted_row = ["dummy"] + row
            word, infinitive, mood, tense, person, number = shifted_row[1], shifted_row[2], shifted_row[5], shifted_row[6], shifted_row[7], shifted_row[8]
            # Let's omit for now the non-indicative moods, and disregard transitivities
            if mood == 'I':
                grammar_file.write(f"V[AGR=[NUM={number.lower()}, PER={person}, TENSE={tense.lower()}], MOOD={mood.lower()}] -> '{word}'\n")
            #grammar_file.write(f"V[AGR=[NUM={number.lower()}, PER={person}, TENSE={tense.lower()}]] -> '{word}'\n")

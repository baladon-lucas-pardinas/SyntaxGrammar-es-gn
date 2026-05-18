### Read: https://www.nltk.org/book/ch09.html
import csv


def write_verb_productions(grammar_file, verb_lexicon, transitivities, subject):
 # Load verb lexical rules from CSV
    with open(verb_lexicon, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            # This is to use the appropriate columns in matched-verbs-guarani.csv
            shifted_row = [row[1]] + row[-12:-3]
            word, infinitive, mood, tense, person, number = shifted_row[1], shifted_row[2], shifted_row[5], shifted_row[6], shifted_row[7], shifted_row[8]
            # Let's omit for now the non-indicative moods and check if subject makes sense
            if mood == 'I' and (subject != 'np' or person == '3'):
                transitivity = transitivities[infinitive]
                if transitivity['transitive']: 
                    grammar_file.write(f"V[AGR=[NUM={number.lower()}, PER={person}, TENSE={tense.lower()}], MOOD={mood.lower()}, SUBCAT='tr'] -> '{word}'\n")
                if transitivity['intransitive']:
                    grammar_file.write(f"V[AGR=[NUM={number.lower()}, PER={person}, TENSE={tense.lower()}], MOOD={mood.lower()}, SUBCAT='intr'] -> '{word}'\n")
                if transitivity['ditransitive']:
                    grammar_file.write(f"V[AGR=[NUM={number.lower()}, PER={person}, TENSE={tense.lower()}], MOOD={mood.lower()}, SUBCAT='di'] -> '{word}'\n")
            #grammar_file.write(f"V[AGR=[NUM={number.lower()}, PER={person}, TENSE={tense.lower()}]] -> '{word}'\n")

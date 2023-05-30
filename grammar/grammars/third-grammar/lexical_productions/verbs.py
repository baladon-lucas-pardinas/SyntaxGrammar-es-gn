### Read: https://www.nltk.org/book/ch09.html
import csv


def write_verb_productions(grammar_file, verb_lexicon, transitivities):
 # Load verb lexical rules from CSV
    with open(verb_lexicon, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            word, infinitive, mood, tense, person, number = row[1], row[2], row[5], row[6], row[7], row[8]
            # Let's omit for now the non-indicative moods
            if mood == 'I':
                transitivity = transitivities[infinitive]
                if transitivity['transitive']: 
                    grammar_file.write(f"V[AGR=[NUM={number.lower()}, PER={person}, TENSE={tense.lower()}], MOOD={mood.lower()}, SUBCAT='tr'] -> '{word}'\n")
                if transitivity['intransitive']:
                    grammar_file.write(f"V[AGR=[NUM={number.lower()}, PER={person}, TENSE={tense.lower()}], MOOD={mood.lower()}, SUBCAT='intr'] -> '{word}'\n")
            #grammar_file.write(f"V[AGR=[NUM={number.lower()}, PER={person}, TENSE={tense.lower()}]] -> '{word}'\n")

### Arguments are the verb and noun lexicon csv files, and the transitivities csv file
### Read: https://www.nltk.org/book/ch09.html

import csv
import sys
from nltk.grammar import FeatureGrammar

def read_arguments():
    if len(sys.argv) > 2:
        return sys.argv[1], sys.argv[2], sys.argv[3]
    else:
        raise Exception("Not enough arguments were provided")
    
def read_transitivities(file_path):
    result = {}
    
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            verb = row[0]
            transitive = row[1] == 'transitive'
            intransitive = row[2] == 'intransitive'
            
            result[verb] = {'transitive': transitive, 'intransitive': intransitive}
    
    return result


[verb_lexicon, noun_lexicon, transitivities_file] = read_arguments()

transitivities = read_transitivities(transitivities_file)

### Read: https://www.nltk.org/book/ch09.html
grammar = """% start S
S[AGR=?a] -> N[AGR=?a] VP[AGR=?a, MOOD=i]
VP[AGR=?a, MOOD=?m] -> V[AGR=?a, MOOD=?m, SUBCAT='tr'] N[AGR=?b] | V[AGR=?a, MOOD=?m, SUBCAT='intr']
# ###################
# Lexical Rules
"""

with open('output.txt', 'w') as grammar_file:
    grammar_file.write(grammar)


with open('output.txt', 'a') as grammar_file:
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

    # Load noun lexical rules from CSV
    with open(noun_lexicon, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            word = row[1]
            gender = row[5]
            number = row[6]
            grammar_file.write(f"\nN[AGR=[GEN={gender.lower()}, NUM={number.lower()}, PER={'3'}]] -> '{word}'")





#gram = FeatureGrammar.fromstring(grammar)

# print(gram)      
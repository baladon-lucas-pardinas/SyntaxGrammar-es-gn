import sys
from nltk.grammar import FeatureGrammar, CFG
from nltk.parse.generate import generate
from nltk.parse import FeatureEarleyChartParser

def read_arguments():
    if len(sys.argv) > 2:
        return sys.argv[1], sys.argv[2]
    else:
        raise Exception("Not enough arguments were provided")

[cfg_grammar_file, feature_grammar_file] = read_arguments()

feature_grammar_string = ''

with open(feature_grammar_file, 'r') as file:
    chunk_size = 1024  # read 1 KB at a time
    while True:
        chunk = file.read(chunk_size)
        if not chunk:
            break  # end of file
        feature_grammar_string += chunk

feat_gram = FeatureGrammar.fromstring(feature_grammar_string)

cfg_grammar = ''

with open(cfg_grammar_file, 'r') as file:
    chunk_size = 1024  # read 1 KB at a time
    while True:
        chunk = file.read(chunk_size)
        if not chunk:
            break  # end of file
        cfg_grammar += chunk

cfg_gram = CFG.fromstring(cfg_grammar)

parser = FeatureEarleyChartParser(feat_gram)

with open('output.txt', 'w') as file:
    for sentence in generate(cfg_gram, None, None, 1000):
        if parser.parse_one(sentence):
            file.write(' '.join(sentence) + '\n')

print("OK")
### Usage: python custom-generate-sentences.py <cfg-grammar-file> <feature-grammar-file>

### Inspired by https://eli.thegreenplace.net/2010/01/28/generating-random-sentences-from-a-context-free-grammar/
from collections import defaultdict
import random
import sys
from nltk.grammar import FeatureGrammar
from nltk.parse import FeatureEarleyChartParser

class CFG(object):
    def __init__(self):
        self.prod = defaultdict(list)

    def add_prod(self, lhs, rhs):
        """ Add production to the grammar. 'rhs' can
            be several productions separated by '|'.
            Each production is a sequence of symbols
            separated by whitespace.

            Usage:
                grammar.add_prod('NT', 'VP PP')
                grammar.add_prod('Digit', '1|2|3|4')
        """
        prods = rhs.split('|')
        for prod in prods:
            self.prod[lhs].append(tuple(prod.split()))

    def gen_random(self, symbol):
        """ Generate a random sentence from the
            grammar, starting with the given
            symbol.
        """
        sentence = []

        # select one production of this symbol randomly
        rand_prod = random.choice(self.prod[symbol])

        for sym in rand_prod:
            # for non-terminals, recurse
            if sym in self.prod:
                sentence.append(self.gen_random(sym))
            else:
                sentence.append(sym)

        return ' '.join(sentence) # Could perhaps return a list, but parser complains
    
def read_arguments():
    if len(sys.argv) > 2:
        return sys.argv[1], sys.argv[2]
    else:
        raise Exception("Not enough arguments were provided")


def isRule(line: str):
    return (not not line) and not line.startswith("#") and not line.startswith("%")

def load_cfg_grammar(grammar_file):
    grammar = CFG()
    with open(grammar_file, "r") as file: 
        for line in file: # type: str
            line = line.strip()  # Remove leading/trailing whitespace
            if (isRule(line)):
                lhs, rhs = line.split("->")
                lhs = lhs.strip()
                rhs = rhs.replace("'", "").replace('"', '').strip()
                grammar.add_prod(lhs, rhs)
    return grammar

def load_feature_grammar(grammar_file):
    feature_grammar_string = ''

    with open(grammar_file, 'r') as file:
        chunk_size = 1024  # read 1 KB at a time
        i = 0
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break  # end of file
            feature_grammar_string += chunk

    return FeatureGrammar.fromstring(feature_grammar_string)



def main():
    [cfg_grammar_file, feature_grammar_file] = read_arguments()
    
    cfg_grammar = load_cfg_grammar(cfg_grammar_file)
    feat_grammar = load_feature_grammar(feature_grammar_file)
    parser = FeatureEarleyChartParser(feat_grammar)


    with open('output.txt', 'w') as file:
        for i in range(10000):
            sentence = cfg_grammar.gen_random('S')
            # print(sentence)
            # if sentence and parser.parse_one(sentence.split(" ")):
            if sentence:
                file.write(sentence + '\n')

        

if __name__ == '__main__':
    main()
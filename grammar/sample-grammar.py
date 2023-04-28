# Escriba su gramática aquí

################
# Perhaps read this: https://stackoverflow.com/questions/15009656/how-to-use-nltk-to-generate-sentences-from-an-induced-grammar
################
from nltk.grammar import FeatStructNonterminal, FeatureGrammar
from nltk import grammar, parse
from nltk.parse import ChartParser
import random

grammar = '''

% start S

#####################
# Grammar Rules

S -> NP[AGR=?a] V[AGR=?a, COMPS=[]]

NP[AGR=?a] -> NP[AGR=?a] RP[COMPS=[vp]] V[AGR=?a, COMPS=[]]

NP[AGR=?a, COMPS=[]] -> D[AGR=?a] N[AGR=?a, COMPS=[]]
NP[AGR=?a, COMPS=[]] -> N[AGR=?a, COMPS=[]]

N[AGR=?a, COMPS=[]] -> N[AGR=?a, COMPS=[pp]] PP
N[AGR=?a, COMPS=[]] -> N[AGR=?a, COMPS=[]] PP

PP[COMPS=[]] -> P[COMPS=[np]] NP

V[AGR=?a, COMPS=[]] -> V[AGR=?a, COMPS=[np]] NP
V[AGR=?a, COMPS=[]] -> V[AGR=?a, COMPS=[pp, pp]] PP PP

V[AGR=?a, COMPS=[]] -> V[AGR=?a, COMPS=[]] PP


# ###################
# Lexical Rules

D[AGR=[GEN=m, NUM=sg]]  -> 'el' | 'un'
D[AGR=[GEN=m, NUM=pl]]  -> 'los' | 'unos'
D[AGR=[GEN=f, NUM=sg]]  -> 'la' | 'una'
D[AGR=[GEN=f, NUM=pl]]  -> 'las' | 'unas'
D[AGR=[NUM=sg]]  -> 'su' | 'mi'

N[AGR=[GEN=m, NUM=sg, PER=ter], COMPS=[]] -> 'niño' | 'barrio' | 'vecino'
N[AGR=[GEN=m, NUM=sg, PER=ter], COMPS=[pp]] -> 'guiso'
N[AGR=[GEN=f, NUM=sg, PER=ter], COMPS=[]] -> 'casa' | 'manzana' | 'escuela' | 'tarde'
N[AGR=[GEN=f, NUM=pl, PER=ter], COMPS=[]] -> 'lentejas'

V[AGR=[NUM=sg, PER=ter], COMPS=[pp, pp]] -> 'vuelve'
V[AGR=[NUM=sg, PER=ter], COMPS=[np]] -> 'come' | 'es'

P[COMPS=[np]] -> 'de' | 'para'

RP[COMPS=[vp]] -> 'que'

'''

gram = FeatureGrammar.fromstring(grammar) 

# parser = parse.FeatureEarleyChartParser(gram)

# trees = list(parser.parse(['el', 'niño', 'come', 'una', 'manzana']))

# for tree in trees:
#     print(tree)

parser = ChartParser(gram)

sentences = set()

# generate up to 10 sentences
while len(sentences) < 3:
    sentence = ' '.join(random.choice(['niño', 'guiso', 'lentejas']) + ' ' + random.choice(['vuelve', 'come', 'es']) for _ in range(random.randint(1, 5)))
    trees = list(parser.parse(sentence.split()))
    if trees:
        words = [leaf[0] for tree in trees for leaf in tree.leaves()]
        sentences.add(' '.join(words))

print('\n'.join(sentences))
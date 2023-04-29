# Escriba su gramática aquí

################
# Perhaps read this: https://stackoverflow.com/questions/15009656/how-to-use-nltk-to-generate-sentences-from-an-induced-grammar
################
from nltk.grammar import FeatStructNonterminal, FeatureGrammar
from nltk import grammar, parse
from nltk.parse import ChartParser
from nltk.parse.generate import generate

feat_grammar = '''

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
N[AGR=[GEN=m, NUM=pl, PER=ter], COMPS=[]] -> 'niños'

V[AGR=[NUM=pl, PER=ter], COMPS=[pp, pp]] -> 'vuelven'
V[AGR=[NUM=sg, PER=ter], COMPS=[np]] -> 'come' | 'es'

V[AGR=[NUM=pl, PER=ter], COMPS=[]] -> 'son'
V[AGR=[NUM=sg, PER=ter], COMPS=[]] -> 'vive'

P[COMPS=[np]] -> 'de' | 'para'

RP[COMPS=[vp]] -> 'que'

'''

cfg_grammar = '''

% start S

#####################
# Grammar Rules

S -> NP V

NP -> D N


# ###################
# Lexical Rules

D  -> 'el'
D  -> 'los'
D  -> 'la'
D  -> 'las'

N -> 'niños'
N -> 'barrio'
N -> 'casa'
N -> 'lentejas'

V -> 'son'
V -> 'vive'


'''

feat_gram = FeatureGrammar.fromstring(feat_grammar) 

cfg_gram = grammar.CFG.fromstring(cfg_grammar)


# parser = ChartParser(feat_gram)

sentences = set()

parser = parse.FeatureEarleyChartParser(feat_gram)


# for tree in trees:
#     print(tree)

trees = list(parser.parse(['el', 'niño', 'come', 'una', 'manzana']))

# print('\n'.join(sentences))

for sentence in generate(cfg_gram):
    if parser.parse_one(sentence):
        sentences.add(' '.join(sentence))

print('\n'.join(sentences))
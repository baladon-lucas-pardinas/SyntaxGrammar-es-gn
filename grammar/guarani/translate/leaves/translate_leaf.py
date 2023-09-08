from .nouns import translate_nouns
from .verbs import translate_verbs
from .aa import translate_aa
from .pronouns import translate_pronouns
from .adpositions import translate_adpositions
from .determiners import translate_determiners
from .adjectives import translate_adjectives
from .connectors import translate_connectors

def translate_leaf(spanish_tree, lexicon): 
    symbol = spanish_tree['type']
    if (symbol == 'D'):
        return translate_determiners(spanish_tree, lexicon['D'])
    if (symbol == 'N'):
        return translate_nouns(spanish_tree, lexicon['N'])
    if (symbol == 'V'):
        return translate_verbs(spanish_tree, lexicon['V'])
    if (symbol == 'A'):
        return translate_adjectives(spanish_tree, lexicon['A'])
    if (symbol == 'P'):
        return translate_pronouns(spanish_tree, lexicon['P'])
    if (symbol == 'PR'):
        return translate_adpositions(spanish_tree, lexicon['PR'])
    if (symbol == 'AA'):
        return translate_aa(spanish_tree, lexicon['AA'])
    if (symbol == 'A'):
        return translate_adjectives(spanish_tree, lexicon['A'])
    if (symbol == 'C'):
        return translate_connectors(spanish_tree, lexicon['C'])
    if (symbol == 'NEG'):
        return []
    raise Exception("Error: symbol not found in lexicon - " + symbol)
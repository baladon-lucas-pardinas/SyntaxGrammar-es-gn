from .nouns import translate_nouns
from .verbs import translate_verbs
from .determiners import translate_determiners

def translate_leaf(spanish_tree, lexicon): 
    symbol = spanish_tree['type']
    if (symbol == 'D'):
        return translate_determiners(spanish_tree, lexicon['D'])
    if (symbol == 'N'):
        return translate_nouns(spanish_tree, lexicon['N'])
    if (symbol == 'V'):
        return translate_verbs(spanish_tree, lexicon['V'])
    raise Exception("Error: symbol not found in lexicon - " + symbol)
from .aa import translate_aa
from .adjectives import translate_adjectives
from .adpositions import translate_adpositions
from .adverbs import translate_adverbs
from .connectors import translate_connectors
from .determiners import translate_determiners
from .nouns import translate_nouns
from .pronouns import translate_pronouns
from .verbs import translate_verbs


def translate_leaf(spanish_tree, lexicon):
    symbol = spanish_tree["type"]
    if symbol == "D":
        return translate_determiners(spanish_tree, lexicon["D"])
    if symbol == "N":
        return translate_nouns(spanish_tree, lexicon["N"])
    if symbol == "V":
        return translate_verbs(spanish_tree, lexicon["V"])
    if symbol == "A":
        return translate_adjectives(spanish_tree, lexicon["A"])
    if symbol == "P":
        return translate_pronouns(spanish_tree, lexicon["P"])
    if symbol == "PR":
        return translate_adpositions(spanish_tree, lexicon["PR"])
    if symbol == "AA":
        return translate_aa(spanish_tree, lexicon["AA"])
    if symbol == "R":
        return translate_adverbs(spanish_tree, lexicon["R"])
    if symbol == "A":
        return translate_adjectives(spanish_tree, lexicon["A"])
    if symbol == "CON":
        return translate_connectors(spanish_tree, lexicon["CON"])
    if symbol == "NEG":
        return []
    raise Exception("Error: symbol not found in lexicon - " + symbol)

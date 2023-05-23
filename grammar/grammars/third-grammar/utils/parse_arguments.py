import argparse


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('verbs', type=str, help='Path to the verb lexicon')
    parser.add_argument('nouns', type=str, help='Path to the noun lexicon')
    parser.add_argument('transitivities', type=str, help='Path to the transitivities file')
    parser.add_argument('-r', '--adverbs', type=str, help='Path to the adverb lexicon')
    parser.add_argument('-a', '--adjectives', type=str, help='Path to the adjective lexicon')
    parser.add_argument('-d', '--determinants', type=str, help='Path to the determinant lexicon')
    parser.add_argument('-p', '--pronouns', type=str, help='Path to the pronoun lexicon')
    parser.add_argument('-s', '--adpositions', type=str, help='Path to the preposition lexicon')
    parser.add_argument('-o', '--output', type=str, default='output.txt', help='Path to the output file')


    return parser.parse_args()
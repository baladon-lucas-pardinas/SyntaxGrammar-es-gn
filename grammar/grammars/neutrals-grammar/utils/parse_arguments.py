import argparse


def parse_arguments():
    parser = argparse.ArgumentParser()

    # parser.add_argument('verbs', type=str, help='Path to the verb lexicon')
    # parser.add_argument('nouns', type=str, help='Path to the noun lexicon')
    # parser.add_argument('transitivities', type=str, help='Path to the transitivities file')
    # parser.add_argument('-r', '--adverbs', type=str, help='Path to the adverb lexicon')
    # parser.add_argument('-a', '--adjectives', type=str, help='Path to the adjective lexicon')
    # parser.add_argument('-d', '--determiners', type=str, help='Path to the determiner lexicon')
    # parser.add_argument('-p', '--pronouns', type=str, help='Path to the pronoun lexicon')
    # parser.add_argument('-s', '--adpositions', type=str, help='Path to the preposition lexicon')
    # parser.add_argument('-o', '--output', type=str, default='output.txt', help='Path to the output file')
    parser.add_argument('-c', '--config', type=str, default='config.yaml', help='Path to the config file')
    parser.add_argument('-s', '--subject', type=str, default='np', help='Subject type (np, adj or pronoun)')

    return parser.parse_args()
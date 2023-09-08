import random
from .fetch.spanish_trees import fetch_spanish_trees
from .fetch.syntactic_transfer_rules import fetch_syntactic_transfer_rules
from .utils.read_csv import read_csv
from .utils.write_csv import write_to_csv
from .utils.parse_arguments import parse_arguments
from .corpus_generation.remove_duplicates import remove_duplicates
from .transfer.guarani_tree import build_guarani_tree
from .corpus_generation.extract_words import extract_words
from .corpus_generation.post_process import post_process
   
def main():
    # Get CSV files
    nouns = read_csv("../../guarani/nouns/finished-nouns.csv")
    determiners = read_csv("../../guarani/determiners/determiners.csv")
    adjectives = read_csv("../../guarani/adjectives/matched-adjectives-guarani.csv")
    pronouns = read_csv("../../guarani/pronouns/pronouns.csv")
    verbs = read_csv("../../guarani/verbs/matched-verbs-guarani.csv")
    adpositions = read_csv("../../guarani/adpositions/adpositions.csv")
    connectors = read_csv("../../guarani/connectors/connectors.csv")

    lexicon = {
        'N' : nouns,
        'D' : determiners,
        'A' : adjectives,
        'P' : pronouns,
        'V' : verbs,
        'AA': adpositions,
        'PR': adpositions,
        'C': connectors
    }

    args = parse_arguments()
    trees = fetch_spanish_trees(args.spanish_trees_file)
    transfer_rules = fetch_syntactic_transfer_rules(args.equivalence_rules_file)
    parallel_corpus = []

    for spanish_tree in trees:
        translations = build_guarani_tree(spanish_tree, transfer_rules, lexicon)
        spanish_sentence = extract_words(spanish_tree)

        if translations == []:
            print(spanish_sentence)
            
        # pick three translations at random
        translations = random.sample(translations, min(args.max_translations, len(translations)))

        for (guarani_sentence, features) in translations:
            sentence_pair = post_process([spanish_sentence, guarani_sentence])
            parallel_corpus.append(sentence_pair)

    write_to_csv(args.output, parallel_corpus)
    # remove_duplicates(args.output)

if __name__ == '__main__':
    main()
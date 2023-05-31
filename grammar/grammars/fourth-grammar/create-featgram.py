### Usage: python create-featgram.py --help

from lexical_productions.verbs import write_verb_productions
from lexical_productions.nouns import write_noun_productions
from lexical_productions.determiners import write_determiner_productions
from lexical_productions.pronouns import write_pronoun_productions
from utils.parse_arguments import parse_arguments
from utils.read_transitivities import read_transitivities
from grammar_productions.grammar_string import grammar as base_grammar_string

def main():

    args = parse_arguments()
    [verb_lexicon, noun_lexicon, transitivities_file] = [args.verbs, args.nouns, args.transitivities]
    output_file = args.output

    transitivities = read_transitivities(transitivities_file)


    with open(output_file, 'w') as grammar_file:
        grammar_file.write(base_grammar_string)

    with open(output_file, 'a') as grammar_file:
        write_verb_productions(grammar_file, verb_lexicon, transitivities)
        write_noun_productions(grammar_file, noun_lexicon)
        if args.determiners:
            write_determiner_productions(grammar_file, args.determiners)
        if args.pronouns:
            write_pronoun_productions(grammar_file, args.pronouns)
        


if __name__ == '__main__':
    main()
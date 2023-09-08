### Usage: python create-featgram.py --help

from .utils.parse_arguments import parse_arguments
from .lexical_productions.verbs import write_verb_productions
from .lexical_productions.nouns import write_noun_productions
from .lexical_productions.determiners import write_determiner_productions
from .lexical_productions.pronouns import write_pronoun_productions
from .lexical_productions.adpositions import write_adposition_productions
from .lexical_productions.adjectives import write_adjective_productions
from .lexical_productions.connectors import write_connector_productions
from .utils.read_config import read_config
from .utils.read_transitivities import read_transitivities
from .grammar_productions.ancora_grammar import grammar as ancora_grammar_string
from .utils.remove_duplicates import remove_duplicates

def main():
    args = parse_arguments()
    config = read_config(args.config)
    [verb_lexicon, noun_lexicon, transitivities_file] = [config['verbs'], config['nouns'], config['transitivities']]
    output_file = config['output']

    transitivities = read_transitivities(transitivities_file)

    
    base_grammar_string = ancora_grammar_string

    with open(output_file, 'w') as grammar_file:
        grammar_file.write(base_grammar_string)

    with open(output_file, 'a') as grammar_file:
        write_verb_productions(grammar_file, verb_lexicon, transitivities)
        write_noun_productions(grammar_file, noun_lexicon)
        if 'determiners' in config:
            write_determiner_productions(grammar_file, config['determiners'])
        if 'pronouns' in config:
            write_pronoun_productions(grammar_file, config['pronouns'])
        if 'adpositions' in config:
            write_adposition_productions(grammar_file, config['adpositions'])
        if 'adjectives' in config:
            write_adjective_productions(grammar_file, config['adjectives'])
        if 'connectors' in config:
            write_connector_productions(grammar_file, config['connectors'])

    remove_duplicates(output_file)


if __name__ == '__main__':
    main()
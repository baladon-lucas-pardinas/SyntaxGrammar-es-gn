from nltk import grammar, FeatureChartParser
### WHAT I SHOULD DO HERE INSTEAD IS SPLIT BY UNKNOWN WORDS AND THEN PARSE EACH SUBSTRING
### I SHOULD READ FROM MY EXTRACTED.CSV
### FOR PARSING EACH SUBSTRING I SHOULD DO A SORT OF MAXMATCH, BUT THAT CAN BE ANOTHER SCRIPT, V3

# Define your grammar rules here
grammar_rules = """
    S -> NP VP
    NP -> Det N
    VP -> V NP | V
    Det -> 'the' | 'a'
    N -> 'dog' | 'cat'
    V -> 'chased' | 'slept'
"""
my_grammar = grammar.FeatureGrammar.fromstring(grammar_rules)

# Create a FeatureChartParser instance
parser = FeatureChartParser(my_grammar)

def partial_parse(sentence):
    words = sentence.split()
    partial_trees = []
    s_parse_found = False
    start_index = 0

    for i in range(len(words)):
        if words[i] not in my_grammar._lexical_index:
            if i > start_index:
                substring = " ".join(words[start_index:i])
                parses = list(parser.parse(substring.split()))
                if parses:
                    if parses[-1].label() == 'S':
                        s_parse_found = True
                    partial_trees.append((substring, parses[-1]))
            start_index = i + 1

    # Parse the last segment if it's not fully covered
    if start_index < len(words):
        substring = " ".join(words[start_index:])
        parses = list(parser.parse(substring.split()))
        if parses:
            if parses[-1].label() == 'S':
                s_parse_found = True
            partial_trees.append((substring, parses[-1]))

    return partial_trees

sentence = "the dog chased the cat and the cat slept and the cat chased and the dog slept"
partial_results = partial_parse(sentence)

for substring, parse_tree in partial_results:
    print(f"Partial parse for '{substring}':")
    print(parse_tree)
    print()

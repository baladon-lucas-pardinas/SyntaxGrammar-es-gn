import argparse
import csv
from nltk import grammar, FeatureChartParser, Tree
import re

# Function to read a text file into a string
def read_text_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()


def find_last_substring_with_whitespace(sub_sentence, substring):
    pattern = r'\b' + re.escape(substring) + r'(?=\s|$)'
    matches = list(re.finditer(pattern, sub_sentence))
    if matches:
        last_match = matches[-1]
        return last_match.start()
    else:
        return -1  # Return -1 when the substring is not found


# Function to read sentences from a CSV file into a list
def read_sentences_from_csv(file_path):
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        return [row[0] for row in csv_reader] # Assuming single-column CSV

# Function to split sentences
def split_sentence(sentence: str, grammar: grammar.FeatureGrammar) -> list[str]:
    words = sentence.split()  # Split the sentence into words
    sub_sentences = []
    current_sub_sentence = []
    for word in words:
        if word in grammar._lexical_index:  # Check if the word is known in the grammar
            current_sub_sentence.append(word)
        else:
            if  len(current_sub_sentence) > 1:  # Append current sub_sentence if at least 2 words
                sub_sentences.append(" ".join(current_sub_sentence))
            current_sub_sentence = []

    if len(current_sub_sentence) > 1:  # Append the last sub_sentence if at least 2 words
        sub_sentences.append(" ".join(current_sub_sentence))

    return sub_sentences

# Function to find the longest substring that can be parsed and return its parse tree
# Recursively does the same for each remaining string (ie. left and right of the parsed substring)
def max_tree(sub_sentence: str, feature_parser: FeatureChartParser) -> list[tuple[Tree, int, int]]:
    words = sub_sentence.split()
    substrings = []
    result = []

    # Generate all possible substrings, excluding single-word substrings, in order of longest to shortest
    for j in range(len(words), 0, -1):
        for i in range(len(words) - j + 1):
            substring = " ".join(words[i:i+j])
            substrings.append(substring)

    # Try parsing each substring and return the first successful tree
    for substring in substrings:
        tree = None
        if ' ' in substring:  # If the substring is not a single word
            tree = feature_parser.parse_one(substring.split())
        else:
            tree = feature_parser.parse_one([substring])
        if tree is not None:
            start_index = find_last_substring_with_whitespace(sub_sentence, substring)
            end_index = start_index + len(substring)
            if (start_index > 0):
                result += max_tree(sub_sentence[:start_index], feature_parser)
            result += [(tree, start_index, end_index)]  # Return a tuple containing the tree and the substring indices
            if (end_index < len(sub_sentence)):
                result += [(x, end_index + y, end_index + z) for (x, y, z) in max_tree(sub_sentence[end_index:], feature_parser)]
            return result

    return []  # Return None if no successful parse tree is found

# Function to write trees to a txt file
def write_trees_to_file(trees, output_file):
    with open(output_file, 'w') as file:
        file.writelines([str(tree) + '\n' for tree in trees])

# Function to write lines to a txt file
def write_sentences_to_file(sentences: list[str], output_file: str):
    with open(output_file, 'w') as file:
        file.writelines([sentence + '\n' for sentence in sentences])

def parse_arguments():
    parser = argparse.ArgumentParser(description='Process sentences using a FeatureChartParser')
    parser.add_argument('--grammar', required=True, help='Path to the feature grammar text file')
    parser.add_argument('--input', required=True, help='Path to the input CSV file containing sentences')
    parser.add_argument('--output', required=True, help='Path to the output txt file for trees')
    parser.add_argument('--indices', required=True, help='Path to the output CSV file for indices')
    parser.add_argument('--nonparsed', help='Path to the output txt file for unmatched sentences')
    return parser.parse_args()

def main():
    args = parse_arguments()

    # Read the feature grammar from a file and create a feature grammar
    grammar_string = read_text_file(args.grammar)
    feat_grammar = grammar.FeatureGrammar.fromstring(grammar_string)

    # Create a FeatureChartParser based on the grammar
    feature_parser = FeatureChartParser(feat_grammar)

    # Read sentences from the CSV file
    sentences = read_sentences_from_csv(args.input)

    # Initialize a list to store trees
    trees = []

    # Initialize a list to store non-parsed sentences
    non_parsed_sentences = []

    # Loop through sentences, split them, and perform max_tree
    for sentence_index, sentence in enumerate(sentences):
        sub_sentences = split_sentence(sentence, feat_grammar)
        current_index = 0  # Initialize the current index
        for sub_sentence in sub_sentences:
            start_index = sentence.find(sub_sentence, current_index)
            end_index = start_index + len(sub_sentence)
            current_index = end_index  # Update the current index for the next iteration
            sub_trees = max_tree(sub_sentence, feature_parser)
            if len(sub_trees) > 0:
                # Append a tuple containing the tree, sentence index, and subsentence indices
                # start_index is inclusive, end_index is exclusive
                for (tree, sub_start_index, sub_end_index) in sub_trees:
                    trees.append((tree, (sentence_index, start_index + sub_start_index, start_index + sub_end_index)))
            else:
                non_parsed_sentences.append(sub_sentence)

    # Write trees to the output txt file
    write_trees_to_file([x[0] for x in trees], args.output)

    # Write sentence indices to a CSV file
    with open(args.indices, 'w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows([x[1] for x in trees])


    # Write sentences we couldn't parse to a different file
    if (args.nonparsed):
        write_sentences_to_file(non_parsed_sentences, args.nonparsed)


if __name__ == '__main__':
    main()

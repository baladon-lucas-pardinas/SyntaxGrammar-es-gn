import argparse
import csv
from nltk import grammar, FeatureChartParser, Tree

### FOR PARSING EACH SUBSTRING I SHOULD DO A SORT OF MAXMATCH, BUT THAT CAN BE ANOTHER SCRIPT, V3

# Function to read a text file into a string
def read_text_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

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

# Function to perform the max_match operation (placeholder, implement later)
def max_match(sentence: str, feature_parser: FeatureChartParser) -> Tree | None:
    # Placeholder, nothing like max_match at all
    return feature_parser.parse_one(sentence.split(" "))

# Function to write trees to a txt file
def write_trees_to_file(trees, output_file):
    with open(output_file, 'w') as file:
        for tree in trees:
            file.write(str(tree) + '\n')

def parse_arguments():
    parser = argparse.ArgumentParser(description='Process sentences using a FeatureChartParser')
    parser.add_argument('--grammar', required=True, help='Path to the feature grammar text file')
    parser.add_argument('--input', required=True, help='Path to the input CSV file containing sentences')
    parser.add_argument('--output', required=True, help='Path to the output txt file for trees')
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

    # Loop through sentences, split them, and perform max_match
    for sentence in sentences:
        sub_sentences = split_sentence(sentence, feat_grammar)
        for sub_sentence in sub_sentences:
            tree = max_match(sub_sentence, feature_parser)
            if tree is not None:
                trees.append(tree)

    # Write trees to the output txt file
    write_trees_to_file(trees, args.output)

if __name__ == '__main__':
    main()
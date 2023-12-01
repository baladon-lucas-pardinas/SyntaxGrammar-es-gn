import argparse


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('spanish_trees_file', type=str, help='Path to the spanish trees file')
    parser.add_argument('equivalence_rules_file', type=str, help='Path to the equivalence rules file')
    parser.add_argument('-o', '--output', type=str, default='output.csv', help='Path to the output file')
    parser.add_argument('-n', '--max-translations', type=int, default=1, help='Maximum number of translations to generate for a single tree (default 1)')
    parser.add_argument('-i', '--indices', type=str, help='Path to the indices CSV file (only for Ancora)')

    return parser.parse_args()
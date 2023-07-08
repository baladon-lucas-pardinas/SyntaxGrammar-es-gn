import argparse


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('spanish_trees_file', type=str, help='Path to the spanish trees file')
    parser.add_argument('equivalence_rules_file', type=str, help='Path to the equivalence rules file')
    parser.add_argument('-o', '--output', type=str, default='output.csv', help='Path to the output file')

    return parser.parse_args()
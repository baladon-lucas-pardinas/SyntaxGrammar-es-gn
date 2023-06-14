import argparse
import csv

def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('spanish_trees_file', type=str, help='Path to the spanish trees file')
    parser.add_argument('equivalence_rules_file', type=str, help='Path to the equivalence rules file')
    parser.add_argument('-o', '--output', type=str, default='output.txt', help='Path to the output file')

    return parser.parse_args()

def read_csv(filepath):
    with open(filepath, 'r') as file:
        reader = csv.reader(file)
        matrix = []
        for row in reader:
            matrix.append(row)
        return matrix
    
def get_syntactic_transfer_rules(filepath):
    # dummy
    rules = {
        'S[AGR=?a] -> NP[AGR=?a] VP[AGR=?a, MOOD=i]' : 'S[AGR=?a] -> NP[AGR=?a] VP[AGR=?a, MOOD=i]',
        "VP[AGR=?a, MOOD=?m] -> V[AGR=?a, MOOD=?m, SUBCAT='intr']" : "VP[AGR=?a, MOOD=?m] -> V[AGR=?a, MOOD=?m, SUBCAT='intr']",
        "VP[AGR=?a, MOOD=?m] -> V[AGR=?a, MOOD=?m, SUBCAT='tr'] NP[AGR=?b]" : "VP[AGR=?a, MOOD=?m] -> V[AGR=?a, MOOD=?m, SUBCAT='tr']",
        "NP[AGR=?a] -> D[AGR=?a] N[AGR=?a]" : "NP[AGR=?a] -> D[AGR=?a] N[AGR=?a] DUMMY_GUARANI_WORKS",
    }
    return rules

def parse_tree(tree_str):
    stack = []
    current_node = None
    principio = False
    termino = False

    for char in tree_str:
        if char == "(":
            if current_node is not None:
                stack.append(current_node)
            current_node = {'type': '', 'label': '', 'children': [], 'word': ''}
            principio = True
            termino = False
        elif char == ")":
            if stack:
                parent_node = stack.pop()
                parent_node['children'].append(current_node)
                current_node = parent_node
                termino = False
        elif char == "[":
            termino = False
            principio = False
        elif char == "]":
            termino = True
        else:
            if principio and not str.isspace(char):
                current_node['type'] += char
            elif termino and not str.isspace(char):
                if char == ',':
                    current_node['label'] += char
                    termino = False
                else:
                    current_node['word'] += char
            elif not str.isspace(char):
                current_node['label'] += char

    return current_node

def get_spanish_trees(filepath):
    with open(filepath, 'r') as file:
        content = file.read()

        trees = []
        tree_start = -1
        stack = []

        for i, char in enumerate(content):
            if char == '(':
                if not stack:
                    tree_start = i
                stack.append('(')
            elif char == ')':
                if len(stack) == 1:
                    trees.append(content[tree_start:i+1])
                stack.pop()

    return [parse_tree(x) for x in trees]

def main():
    args = parse_arguments()
    trees = get_spanish_trees(args.spanish_trees_file)
    # print(trees[0])
    
    ### Next steps: 
    # get equivalent grammar rules
    # get equivalent lexicon rules
    # perform transformation on tree, rule by rule, top to bottom
    # consolidate guarani sentence
    # write both sentences in parallel as a csv

if __name__ == '__main__':
    main()